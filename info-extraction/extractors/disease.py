from prompts import DISEASE_EXTRACTION_PROMPT
from schemas.disease import MainDiseases
from .base import BaseExtractor


class DiseaseExtractor(BaseExtractor[MainDiseases]):
    def __init__(self, llm):
        super().__init__(llm, MainDiseases)
        self.prompt = DISEASE_EXTRACTION_PROMPT.format(
            user_note=""
        )

    def extract(
        self,
        paper_content: str,
        user_note: str = "",
        get_token_count: bool = False,
        verbose: bool = True
    ) -> MainDiseases:
        self.prompt = DISEASE_EXTRACTION_PROMPT.format(
            user_note=user_note
        )

        return super().extract(
            paper_content=paper_content,
            get_token_count=get_token_count,
            verbose=verbose
        )
