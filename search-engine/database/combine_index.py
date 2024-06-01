from .base import Database
from schemas import SearchItem


class _CombineIndexRepo(Database[SearchItem]):
    def __init__(self):
        super(_CombineIndexRepo, self).__init__(
            "combine_index_demo",
            SearchItem
        )


CombineIndexDao: _CombineIndexRepo = _CombineIndexRepo()

