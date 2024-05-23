from schemas import PaperResponse
from .base import Database


class _PaperRepo(Database[PaperResponse]):
    def __init__(self):
        super(_PaperRepo, self).__init__("paper_demo", PaperResponse)


PaperDao: _PaperRepo = _PaperRepo()
