import os
import re
from time import time
from datetime import datetime
from typing import List, Tuple
from llama_index.core.retrievers import RouterRetriever
from llama_index.core.selectors import PydanticMultiSelector
from llama_index.core.tools import RetrieverTool
from llama_index.core.schema import NodeWithScore, TextNode
from llama_index.core.postprocessor import LLMRerank
from llama_index.core import QueryBundle
from llama_index.llms.openai import OpenAI

from .metadata_index import MetadataIndex
from .main_conclusion_index import MainConclusionIndex
from .disease_index import DiseaseIndex
from .demographic_index import DemographicIndex
from .combine_index import CombineIndex
from database import PaperDao
from prompts.query_refine import QUERY_TRANSFORMRATION

from config import settings
import logging
import yaml
logging.basicConfig(level=logging.INFO)


os.environ["TOKENIZERS_PARALLELISM"] = "true"


def parse_json(json_str, marker="{}"):
    indx = json_str.rfind(marker[1])
    json_str = json_str[:indx+1]

    try:
        return yaml.safe_load(json_str)
    except:
        print("Level 2. Cannot parse json. Refining it...")

    indx = json_str.find(marker[0])
    json_str = json_str[indx:]
    try:
        return yaml.safe_load(json_str)
    except:
        print("Level 2. Cannot parse json. Refining it...")

    return None


def custom_parse_choice_select_answer_fn(
    answer: str, num_choices: int, raise_error: bool = False
) -> Tuple[List[int], List[float]]:
    """parse choice select answer function."""
    # print(answer)
    answer_nums = []
    answer_relevances = []
    answer_lines = answer.split("Answer:")[-1].split("\n")
    for answer_line in answer_lines:
        try:
            line_tokens = answer_line.split(",")
            if len(line_tokens) != 2:
                if not raise_error:
                    continue
                else:
                    raise ValueError(
                        f"Invalid answer line: {answer_line}. "
                        "Answer line must be of the form: "
                        "answer_num: <int>, answer_relevance: <float>"
                    )
            answer_num = int(line_tokens[0].split(":")[1].strip())
            if answer_num > num_choices:
                continue
            answer_nums.append(answer_num)
            # extract just the first digits after the colon.
            _answer_relevance = re.findall(r"\d+", line_tokens[1].split(":")[1].strip())[0]
            answer_relevances.append(float(_answer_relevance))
        except Exception as e:
            # no relevant choices found
            # print("Error", e)
            pass
    return answer_nums, answer_relevances


class SearchEngine:
    def __init__(
        self,
        index_dir: str,
        top_k_candidates: int = 10
    ):
        self.llm = OpenAI(
            model=settings.MODEL_NAME,
            api_key=settings.OPENAI_API_KEY
        )

        self.indices = {
            "metadata": MetadataIndex(),
            "main_conclusion": MainConclusionIndex(),
            "disease": DiseaseIndex(),
            "demographic": DemographicIndex(),
            "combine": DemographicIndex()
        }

        for key, index in self.indices.items():
            st = time()
            print(f"Loading {key} index...")
            index.load_index(
                index_dir=os.path.join(index_dir, key),
                top_k=top_k_candidates
            )
            print(f"Done in {time() - st}.")

    def demographic_str(self, demographic):
        return f"Location: {demographic.location.location}\nGender: {demographic.gender.gender}\nSample size before exclusion: {demographic.sample_size.sample_size_before_exclusion}\nSample size after exclusion: {demographic.sample_size.sample_size_after_exclusion}".strip()

    def paper_to_str(self, paper):
        result = f"Title: {paper.title}"
        result += f"\nJournal: {paper.journal}"
        result += f"\nPublication Year: {paper.publication_year}"
        result += f"\nSummary: {paper.conclusions.main_conclusion.conclusion}"
        result += f"\nDiseases: {', '.join([d.name for d in paper.diseases])}"
        result += f"\n{self.demographic_str(paper.demographic)}"
        return result.strip()

    def process_nodes(self, nodes: List[NodeWithScore]) -> List[NodeWithScore]:
        # sort the score in descending order
        nodes.sort(key=lambda x: x.score, reverse=True)

        # combine paper info
        paper_dict = {}
        for node in nodes:
            paper_id = node.node.metadata["paper_id"]
            if paper_id not in paper_dict:
                paper = PaperDao.get(paper_id)
                paper_dict[paper_id] = [0, self.paper_to_str(paper)]

            paper_dict[paper_id][0] += node.score

        # build paper nodes
        paper_nodes = []
        for k, v in paper_dict.items():
            node = NodeWithScore(
                score=v[0],
                node=TextNode(
                    text=v[1],
                    metadata={
                        "paper_id": k
                    }
                )
            )
            paper_nodes.append(node)
        paper_nodes.sort(key=lambda x: x.score, reverse=True)
        return paper_nodes

    def rerank(self, query: str, nodes: List[NodeWithScore], top_k: int = 5):
        # configure reranker
        reranker = LLMRerank(
            choice_batch_size=10,
            top_n=top_k,
            llm=self.llm,
            parse_choice_select_answer_fn=custom_parse_choice_select_answer_fn
        )

        query_bundle = QueryBundle(query)
        retrieved_nodes = reranker.postprocess_nodes(
            nodes, query_bundle
        )
        return retrieved_nodes

    def query(self, query: str, top_k: int = 5):
        # refine the query in case it is too long and complicated
        prompt = QUERY_TRANSFORMRATION.format(
            time=f"{datetime.now()}",
            query=query
        )
        output = self.llm.complete(prompt)
        refined_query = output.text
        json_output = parse_json(refined_query)

        print("Refine queries")
        print(output)

        nodes = []
        for key, index in self.indices.items():
            if key != "combine":
                sub_query = json_output.get(key, query)
            else:
                sub_query = "Title: " + json_output.get("metadata", "")
                sub_query += "\nDiseases: " + json_output.get("disease", "")
                sub_query += "\n" + json_output.get("demographic", "")
                sub_query += "\n" + json_output.get("main_conclusion", "")

            if len(sub_query.strip()) == 0:
                continue
            nodes += index.retriever.retrieve(sub_query)

        nodes = self.process_nodes(nodes)
        nodes = self.rerank(query, nodes, top_k=top_k)
        return nodes
