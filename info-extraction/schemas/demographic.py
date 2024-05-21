from pydantic import BaseModel, Field, validator


class Location(BaseModel):
    justification: str = Field(description="Quote the content from the article that you use to derive the location of the participants for the experiment.", default="")
    location: str = Field(description="Location of the participants for the experiment (country, state, university, lab, etc.).", default="")

    class Config:
        validate_assignment = True

    @validator('justification')
    def set_justification(cls, value):
        return value or 'Not Available'

    @validator('location')
    def set_location(cls, value):
        return value or 'Not Available'


class SampleSize(BaseModel):
    justification: str = Field(description="Quote the content from the article that you use to derive the sample size of the participants for the experiment.", default="")
    exclusion_criteria: str = Field(description="The criteria used to EXCLUDE the UNQUALIFIED participants.", default="")
    inclusion_criteria: str = Field(description="The criteria used to CHOOSE the qualified participants.", default="")
    sample_size_before_exclusion: int | str = Field(description="The initial number of recruited participants, or same as sample_size_after_exclusion if there are no criteria found.", default="")
    sample_size_after_exclusion: int | str = Field(description="The number of participants in the experiment after exclude the unqualified ones.", default="")

    class Config:
        validate_assignment = True

    @validator('justification')
    def set_justification(cls, value):
        return value or 'Not Available'

    @validator('exclusion_criteria')
    def set_exclusion_criteria(cls, value):
        return value or 'Not Available'

    @validator('inclusion_criteria')
    def set_inclusion_criteria(cls, value):
        return value or 'Not Available'

    @validator('sample_size_before_exclusion')
    def set_sample_size_before_exclusion(cls, value):
        return value or 'Not Available'

    @validator('sample_size_after_exclusion')
    def set_sample_size_after_exclusion(cls, value):
        return value or 'Not Available'


class Gender(BaseModel):
    justification: str = Field(description="Quote the content from the article that you use to derive the gender of the participants for the experiment.", default="")
    gender: str = Field(description="Gender of the participants. Accepted values: MALE, FEMALE or BOTH.", default="")

    class Config:
        validate_assignment = True

    @validator('justification')
    def set_justification(cls, value):
        return value or 'Not Available'

    @validator('gender')
    def set_gender(cls, value):
        return value or 'Not Available'


class Demographic(BaseModel):
    has_participants: bool | str = Field(description="True if there is a conducted experiment by the author and there are invited participants, otherwise, return False", default=False)
    location: Location = Location()
    sample_size: SampleSize = SampleSize()
    gender: Gender = Gender()

    class Config:
        validate_assignment = True

    @validator('has_participants')
    def set_has_participants(cls, value):
        return value or False
