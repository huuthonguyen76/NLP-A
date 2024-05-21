from pydantic import BaseModel
from typing import Generic, TypeVar
import instructor
from config import settings
from utils import remove_ref, split_paper, log_token_report


T = TypeVar('T')


class BaseExtractor(Generic[T]):
    def __init__(self, llm, response_model: BaseModel):
        self.llm = llm
        self.client = instructor.from_openai(self.llm)
        self.prompt = ""
        self.instructor_prompt = 'If the information for the field is not available/mentioned, put "Not Available". ### Content:\n'
        self.response_model = response_model

    def to_pydantic(self, text: str) -> T:
        response = self.client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": f'{self.instructor_prompt}{text}'
                },
            ],
            response_model=self.response_model,
            max_retries=2
        )
        return response

    def extract(
        self,
        paper_content: str,
        get_token_count: bool = False,
        verbose: bool = True
    ) -> T:

        paper_content = remove_ref(paper_content)
        chunks = split_paper(paper_content)
        if verbose:
            print(f"Paper length: {len(paper_content)}")
            print(f"Split paper into {len(chunks)} chunks")

        output_token_count = 0
        input_token_count = 0
        llm_output_full = ""
        for i, chunk in enumerate(chunks):
            response = self.llm.chat.completions.create(
                model=settings.MODEL_NAME,
                messages=[
                    {
                        "role": "system",
                        "content": self.prompt
                    },
                    {
                        "role": "user",
                        "content": f"### Article Content:\n{chunk}"
                    },
                ]
            )

            llm_output = response.choices[0].message.content
            if verbose:
                print(f"\n*********** LLM Output {i+1} / {len(chunks)} ************")
                print(llm_output)

            if len(chunks) > 1:
                llm_output_full = f"# Result from text chunk number {i+1}:\n" + llm_output_full
            llm_output_full += llm_output + "\n"
            if get_token_count:
                # record the token usage
                output_token_count += response.usage.completion_tokens
                input_token_count += response.usage.prompt_tokens

        result = self.to_pydantic(llm_output_full)
        if verbose:
            print(f"\n*********** Pydantic Model Version {i+1} / {len(chunks)} ************")
            print(result)

        if get_token_count:
            output_token_count += result._raw_response.usage.completion_tokens
            input_token_count += result._raw_response.usage.prompt_tokens

            if verbose:
                log_token_report(output_token_count, input_token_count)
                print()
            return result, output_token_count, input_token_count

        return result
