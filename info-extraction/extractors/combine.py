from openai import OpenAI
from config import settings
from .conclusion import ConclusionExtractor
from .demographic import DemographicExtractor
from .disease import DiseaseExtractor
from utils import log_token_report


class InformationExtractor:
    def __init__(self):
        llm = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )
        self.conclusion_extractor = ConclusionExtractor(llm)
        self.disease_extractor = DiseaseExtractor(llm)
        self.demographic_extractor = DemographicExtractor(llm)
        self.output_token_count = 0
        self.input_token_count = 0

    def extract(self, paper_content: str, verbose=True) -> dict:
        output_token_count = 0
        input_token_count = 0
        if verbose:
            print("=" * 20)
            print("Extract Main Conclusion")
            print("=" * 20)
        conclusion, o_c, i_c = self.conclusion_extractor.extract(
            paper_content,
            get_token_count=True
        )
        output_token_count += o_c
        input_token_count += i_c

        if verbose:
            print("=" * 20)
            print("Extract Diseases")
            print("=" * 20)
        diseases, o_c, i_c = self.disease_extractor.extract(
            paper_content,
            get_token_count=True,
            verbose=True
        )
        output_token_count += o_c
        input_token_count += i_c

        if verbose:
            print("=" * 20)
            print("Extract Demographic")
            print("=" * 20)
        demographic, o_c, i_c = self.demographic_extractor.extract(
            paper_content,
            get_token_count=True,
            verbose=True
        )
        output_token_count += o_c
        input_token_count += i_c

        if verbose:
            print("========== Paper Token Report ==========")
            log_token_report(output_token_count, input_token_count)

            self.output_token_count += output_token_count
            self.input_token_count += input_token_count
            print("\n========== Cumulative Token Report ==========")
            log_token_report(self.output_token_count, self.input_token_count)
            print("=" * 40)

        return {
            "conclusions": conclusion.dict(),
            "demographic": demographic.dict(),
            **diseases.dict(),
        }
