from typing import List
from schemas import PaperResponse, SearchItem
from database import MetadataIndexDao
from llama_index.embeddings.instructor import InstructorEmbedding
from .base import BaseIndex


class MetadataIndex(BaseIndex):
    def __init__(self):
        super().__init__(MetadataIndexDao)

        self.node_type = "metadata"
        self.embed_model = InstructorEmbedding(
            model_name="hkunlp/instructor-base",
            text_instruction="Represent the Biology article metadata for retrieval: ",
            query_instruction="Represent the Biology query for retrieving article metadata: "
        )

    def get_text(self, paper: PaperResponse) -> SearchItem:
        return f"Title: {paper.title}\nJournal: {paper.journal}\nPublication Year: {paper.publication_year}".strip()

    def get_search_items(
        self,
        papers: List[PaperResponse]
    ) -> List[SearchItem]:
        papers = [paper for paper in papers if paper.title.strip() != ""]
        return [SearchItem(
            paper_id=paper.id,
            text=self.get_text(paper)
        ) for paper in papers]
