from typing import List
from schemas import PaperResponse, SearchItem
from database import MainConclusionIndexDao
from llama_index.embeddings.instructor import InstructorEmbedding
from .base import BaseIndex


class MainConclusionIndex(BaseIndex):
    def __init__(self):
        super().__init__(MainConclusionIndexDao)

        self.node_type = "conclusion"
        self.embed_model = InstructorEmbedding(
            model_name="hkunlp/instructor-base",
            text_instruction="Represent the Biology article summary for retrieval: ",
            query_instruction="Represent the Biology query for retrieving article summary: "
        )

    def get_text(self, paper: PaperResponse) -> SearchItem:
        return paper.conclusions.main_conclusion.conclusion

    def get_search_items(
        self,
        papers: List[PaperResponse]
    ) -> List[SearchItem]:
        papers = [paper for paper in papers if paper.conclusions.main_conclusion.conclusion.strip() != ""]
        return [SearchItem(
            paper_id=paper.id,
            text=self.get_text(paper)
        ) for paper in papers]
