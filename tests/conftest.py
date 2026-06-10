"""Shared pytest fixtures.

The Flask app is imported lazily inside fixtures so that pure unit tests (which
never request a client) do not trigger the app factory or any DB connection.
A fallback SECRET_KEY is injected so the suite does not depend on a .env file
(e.g. in CI), which CSRF and the signed reset tokens both require.
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

_TEST_SECRET = "test-secret-key-not-used-in-prod"


def _ensure_secret_key(app):
    if not app.config.get("SECRET_KEY"):
        app.config["SECRET_KEY"] = _TEST_SECRET


@pytest.fixture
def flask_app():
    """The application, configured for tests (CSRF and rate limiting off)."""
    from app import app

    _ensure_secret_key(app)
    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        RATELIMIT_ENABLED=False,
    )
    return app


@pytest.fixture
def client(flask_app):
    """Test client with CSRF and rate limiting disabled."""
    return flask_app.test_client()


@pytest.fixture
def csrf_client():
    """Test client with CSRF protection enabled (for CSRF-specific tests)."""
    from app import app

    _ensure_secret_key(app)
    app.config.update(TESTING=True, WTF_CSRF_ENABLED=True, RATELIMIT_ENABLED=False)
    return app.test_client()


@pytest.fixture
def ratelimited_client():
    """Test client with rate limiting enabled (for throttling tests)."""
    from app import app
    from extensions import limiter

    _ensure_secret_key(app)
    app.config.update(TESTING=True, WTF_CSRF_ENABLED=False, RATELIMIT_ENABLED=True)
    limiter.reset()
    return app.test_client()
