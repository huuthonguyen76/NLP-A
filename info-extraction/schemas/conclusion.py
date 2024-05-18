from typing import List
from pydantic import BaseModel, Field, validator


class SectionConclusion(BaseModel):
    section_name: str = Field(description='Name or main topic of the article section', default="")
    conclusion: str = Field(description='Summary or conclusion of the section.', default="")

    class Config:
        validate_assignment = True

    @validator('section_name')
    def set_name(cls, value):
        return value or 'Not Available'

    @validator('conclusion')
    def set_conclusion(cls, value):
        return value or 'Not Available'


class MainConclusion(BaseModel):
    conclusion: str = Field(description='Main conclusion of the whole article', default="")
    justification: str = Field(description='Justification or quote from the article to justify how the conclusion is derived.', default="")

    class Config:
        validate_assignment = True

    @validator('justification')
    def set_justification(cls, value):
        return value or 'Not Available'

    @validator('conclusion')
    def set_conclusion(cls, value):
        return value or 'Not Available'


class Conclusions(BaseModel):
    sections: List[SectionConclusion]
    main_conclusion: MainConclusion
