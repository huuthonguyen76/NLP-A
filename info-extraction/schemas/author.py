from pydantic import BaseModel


class Author(BaseModel):
    name: str = ""
    affiliations: list[str] = []

    def __str__(self):
        return self.name
