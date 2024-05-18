from typing import List
from pydantic import BaseModel, Field, validator


class Disease(BaseModel):
    justification: str = Field(description="Explanation or quote from the article justifying the classification as a main disease.", default="")
    name: str = Field(description="Name of the disease.", default="")
    description: str = Field(description="Formal definition of the disease.", default="")

    class Config:
        validate_assignment = True

    @validator('justification')
    def set_justification(cls, value):
        return value or 'Not Available'

    @validator('name')
    def set_name(cls, value):
        return value or 'Not Available'

    @validator('description')
    def set_description(cls, value):
        return value or 'Not Available'


class MainDiseases(BaseModel):
    diseases: List[Disease]
