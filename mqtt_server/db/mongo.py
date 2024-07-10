import pymongo
from pymongo import MongoClient
from typing import Dict, Any, List, Optional
from config import BaseConfig
from mqtt_server.db.models import Base

class MongoDBHandler:
    """
    This class is used to interact with the MongoDB database.
    """
    def __init__(self, db_name: str = BaseConfig.MONGO_DB, uri: str = BaseConfig.MONGO_URI):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def insert_one(self, collection_name: str, document: Dict[str, Any]) -> None:
        base_data = dict(Base()) # this will create a basic structure for writing data into db
        base_data.update(document) # Updating values from document
        collection = self.db[collection_name]
        collection.insert_one(base_data)

    def find(self, collection_name: str, query: Optional[Dict[str, Any]] = None, skip: int = 0, limit: int = 10, sort_field: Optional[str] = None, sort_order: int = pymongo.ASCENDING) -> List[Dict[str, Any]]:
        collection = self.db[collection_name]
        total_count = collection.count_documents(query or {})
        cursor = collection.find(query or {})  # Use an empty dictionary if query is None
        cursor = cursor.skip(skip).limit(limit)
        if sort_field:
            cursor = cursor.sort(sort_field, sort_order)
        return total_count, [self._sanitize_document(doc) for doc in cursor]

    def count_documents(self, collection_name: str, query: Dict[str, Any]) -> int:
        collection = self.db[collection_name]
        return collection.count_documents(query)

    def _sanitize_document(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """Convert ObjectId to string to avoid serialization issues."""
        if '_id' in document:
            document['_id'] = str(document['_id'])
        return document
