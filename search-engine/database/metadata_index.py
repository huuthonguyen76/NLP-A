from .base import Database
from schemas import SearchItem


class _MetadataIndexRepo(Database[SearchItem]):
    def __init__(self):
        super(_MetadataIndexRepo, self).__init__(
            "metadata_index_demo",
            SearchItem
        )


MetadataIndexDao: _MetadataIndexRepo = _MetadataIndexRepo()
