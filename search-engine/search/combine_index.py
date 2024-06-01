from typing import List
from schemas import PaperResponse, SearchItem, Demographic
from schemas.demographic import SampleSize
from database import CombineIndexDao
from llama_index.embeddings.instructor import InstructorEmbedding
from .base import BaseIndex


class CombineIndex(BaseIndex):
    def __init__(self):
        super().__init__(CombineIndexDao)

        self.node_type = "conclusion"
        self.embed_model = InstructorEmbedding(
            model_name="hkunlp/instructor-base",
            text_instruction="Represent the Biology article information for retrieval: ",
            query_instruction="Represent the Biology query for retrieving article information: "
        )

    def get_sample_size(self, sample_size: SampleSize) -> str:
        if type(sample_size.sample_size_after_exclusion) is int:
            return sample_size.sample_size_after_exclusion

        if type(sample_size.sample_size_before_exclusion) is int:
            return sample_size.sample_size_before_exclusion
        return 0

    def get_demographic(self, demographic: Demographic) -> str:
        return f"Location: {demographic.location.location}\nGender: {demographic.gender.gender}\nSample size: {self.get_sample_size(demographic.sample_size)}".strip()

    def get_diseases(self, paper: PaperResponse) -> str:
        return f"Diseases: {', '.join([d.name for d in paper.diseases])}"

    def get_metadata(self, paper: PaperResponse) -> str:
        return f"Title: {paper.title}\nJournal: {paper.journal}\nPublication Year: {paper.publication_year}".strip()

    def get_conclusion(self, paper: PaperResponse) -> str:
        return paper.conclusions.main_conclusion.conclusion

    def get_text(self, paper: PaperResponse) -> SearchItem:
        result = self.get_metadata(paper)
        result += "\n" + self.get_diseases(paper)
        result += "\n" + self.get_demographic(paper.demographic)
        result += "\n" + self.get_conclusion(paper)
        return result

    def get_search_items(
        self,
        papers: List[PaperResponse]
    ) -> List[SearchItem]:
        papers = [paper for paper in papers if paper.conclusions.main_conclusion.conclusion.strip() != ""]
        return [SearchItem(
            paper_id=paper.id,
            text=self.get_text(paper)
        ) for paper in papers]
