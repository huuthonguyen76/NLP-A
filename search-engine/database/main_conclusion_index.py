from .base import Database
from schemas import SearchItem


class _MainConclusionIndexRepo(Database[SearchItem]):
    def __init__(self):
        super(_MainConclusionIndexRepo, self).__init__(
            "main_conclusion_index_demo",
            SearchItem
        )


MainConclusionIndexDao: _MainConclusionIndexRepo = _MainConclusionIndexRepo()
