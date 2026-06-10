import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import app as _app  # noqa: F401  ensures the factory ran and Mongo is initialised
from extensions import articles_collection


def test_mongo_connection():
    documents = list(articles_collection().find())
    assert isinstance(documents, list)
