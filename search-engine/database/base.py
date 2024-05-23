from typing import Generic, TypeVar, List
from pymongo import MongoClient
from pydantic import BaseModel
from config import settings
from bson import ObjectId


T = TypeVar('T')


class Database(Generic[T]):
    def __init__(self, collection_name: str, pydantic_model: type):
        self.client = MongoClient(settings.MONGODB_URI)
        self.db = self.client[settings.MONGODB_DATABASE_NAME]
        self.collection = self.db[collection_name]
        self.pydantic_model = pydantic_model

    def insert(self, item: BaseModel):
        self.collection.insert_one(item.dict())

    def get(self, id: str) -> T:
        item = self.collection.find_one(filter={
            "_id": ObjectId(id)
        })
        if item is None:
            return None
        model = self.pydantic_model.model_validate(item)
        if "id" in model.__fields__:
            model.id = str(item["_id"])
        return model

    def update(self, id: str, item: dict):
        self.collection.update_one(filter={
            "_id": ObjectId(id)
        }, update={"$set": item})

    def get_all(self) -> List[T]:
        result = self.collection.find()
        if result is None:
            return []

        items = []
        for item in result:
            model = self.pydantic_model.model_validate(item, strict=False)
            if "id" in model.__fields__:
                model.id = str(item["_id"])
            items.append(model)
        return items
