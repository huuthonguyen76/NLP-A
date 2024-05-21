from pydantic import BaseModel
from bson import ObjectId
from .author import Author


class Paper(BaseModel):
    title: str = ""
    doi: str = ""
    pmid: str = ""
    journal: str = ""
    impact_factor: float = -1
    publication_year: str = ""
    authors: list[Author] = []
    paper_link: str = ""
    pdf_link: str = ""
    pdf_file_path: str = ""


# for database
class PaperItem(BaseModel):
    title: str = ""
    doi: str = ""
    pmid: str = ""
    url: str = ""
    journal: str = ""
    impact_factor: float = -1
    publication_year: str = ""
    authors: list[Author] = []
    content: str = ""


class PaperResponse(BaseModel):
    id: str = ""
    title: str = ""
    doi: str = ""
    pmid: str = ""
    url: str = ""
    journal: str = ""
    impact_factor: float = -1
    publication_year: str = ""
    authors: list[Author] = []
    content: str = ""
    main_conclusion: str = ""
