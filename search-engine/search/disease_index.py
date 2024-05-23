from typing import List
from schemas import PaperResponse, SearchItem
from database import DiseaseIndexDao
from llama_index.embeddings.instructor import InstructorEmbedding
from .base import BaseIndex


class DiseaseIndex(BaseIndex):
    def __init__(self):
        super().__init__(DiseaseIndexDao)

        self.node_type = "disease"
        self.embed_model = InstructorEmbedding(
            model_name="hkunlp/instructor-base",
            text_instruction="Represent the Biology disease definition for retrieval: ",
            query_instruction="Represent the Biology query for retrieving diseases: "
        )

    def get_search_items(
        self,
        papers: List[PaperResponse]
    ) -> List[SearchItem]:
        result = []
        ignore_phrases = ["not available", "not applicable"]
        for paper in papers:
            if len(paper.diseases) < 0:
                continue

            for disease in paper.diseases:
                description = disease.description if disease.description.lower() not in ignore_phrases else ""
                result.append(SearchItem(
                    paper_id=paper.id,
                    text=f"{disease.name} {description}".strip()
                ))
        return result
