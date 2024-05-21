from typing import List
from pydantic import BaseModel
from bson import ObjectId
from .author import Author
from .conclusion import Conclusions
from .demographic import Demographic
from .disease import Disease


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
    conclusions: Conclusions = Conclusions()
    demographic: Demographic = Demographic()
    diseases: List[Disease] = []


class Metadata(BaseModel):
    paper_id: str = ""
    title: str = ""
    journal: str = ""
    publication_year: str = ""
    authors: list[Author] = []
    embedding: list[float] = []


class ContentItem(BaseModel):
    paper_id: str = ""
    text_chunk: str = ""
    embedding: list[float] = []


class MainConclusionItem(BaseModel):
    paper_id: str = ""
    text: str = ""
    embedding: list[float] = []
