from prompts import CONCLUSION_EXTRACTION_PROMPT
from .base import BaseExtractor
from schemas.conclusion import Conclusions


class ConclusionExtractor(BaseExtractor[Conclusions]):
    def __init__(self, llm):
        super().__init__(llm, Conclusions)
        self.prompt = CONCLUSION_EXTRACTION_PROMPT
