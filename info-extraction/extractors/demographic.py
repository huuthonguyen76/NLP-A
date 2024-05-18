from schemas.demographic import Demographic
from prompts import DEMOGRAPHIC_EXTRACTION_PROMPT
from .base import BaseExtractor


class DemographicExtractor(BaseExtractor[Demographic]):
    def __init__(self, llm):
        super().__init__(llm, Demographic)
        self.prompt = DEMOGRAPHIC_EXTRACTION_PROMPT.format(
            user_note=""
        )

    def extract(
        self,
        paper_content: str,
        user_note: str = "",
        get_token_count: bool = False,
        verbose: bool = True
    ) -> Demographic:
        self.prompt = DEMOGRAPHIC_EXTRACTION_PROMPT.format(
            user_note=user_note
        )

        return super().extract(
            paper_content=paper_content,
            get_token_count=get_token_count,
            verbose=verbose
        )
