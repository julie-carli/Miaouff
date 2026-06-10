"""Smoke tests checking that both databases are reachable."""


def test_postgres_connection(flask_app):
    from models.models import Category

    with flask_app.app_context():
        assert isinstance(Category.query.all(), list)


def test_mongo_connection(flask_app):
    from extensions import articles_collection

    assert isinstance(list(articles_collection().find()), list)
