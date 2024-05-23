from .base import Database
from schemas import SearchItem


class _DiseaseIndexRepo(Database[SearchItem]):
    def __init__(self):
        super(_DiseaseIndexRepo, self).__init__(
            "disease_index_demo",
            SearchItem
        )


DiseaseIndexDao: _DiseaseIndexRepo = _DiseaseIndexRepo()
