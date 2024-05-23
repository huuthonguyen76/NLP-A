from typing import List
from schemas import PaperResponse, SearchItem, Demographic
from schemas.demographic import SampleSize
from database import DemographicIndexDao
from llama_index.embeddings.instructor import InstructorEmbedding
from .base import BaseIndex


class DemographicIndex(BaseIndex):
    def __init__(self):
        super().__init__(DemographicIndexDao)

        self.node_type = "demographic"
        self.embed_model = InstructorEmbedding(
            model_name="hkunlp/instructor-base",
            text_instruction="Represent the Biology experiment demographic for retrieval: ",
            query_instruction="Represent the Biology query for retrieving experiment demographic: "
        )

    def get_sample_size(self, sample_size: SampleSize) -> str:
        if type(sample_size.sample_size_after_exclusion) is int:
            return sample_size.sample_size_after_exclusion

        if type(sample_size.sample_size_before_exclusion) is int:
            return sample_size.sample_size_before_exclusion
        return 0

    def get_text(self, demographic: Demographic) -> SearchItem:
        return f"Location: {demographic.location.location}\nGender: {demographic.gender.gender}\nSample size: {self.get_sample_size(demographic.sample_size)}".strip()

    def get_search_items(
        self,
        papers: List[PaperResponse]
    ) -> List[SearchItem]:
        papers = [paper for paper in papers if paper.demographic.has_participants == True]
        return [SearchItem(
            paper_id=paper.id,
            text=self.get_text(paper.demographic)
        ) for paper in papers]
