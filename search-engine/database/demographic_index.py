from .base import Database
from schemas import SearchItem


class _DemographicIndexRepo(Database[SearchItem]):
    def __init__(self):
        super(_DemographicIndexRepo, self).__init__(
            "demographic_index_demo",
            SearchItem
        )


DemographicIndexDao: _DemographicIndexRepo = _DemographicIndexRepo()
