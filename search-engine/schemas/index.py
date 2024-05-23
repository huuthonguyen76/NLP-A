from pydantic import BaseModel


class SearchItem(BaseModel):
    paper_id: str = ""
    text: str = ""
    embedding: list[float] = []
