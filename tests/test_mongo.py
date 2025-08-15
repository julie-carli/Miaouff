import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import mongo_db


def test_mongo_connection():
    collection = mongo_db.miaouff_collection
    documents = list(collection.find())
    assert isinstance(documents, list)
