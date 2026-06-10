"""Shared pytest configuration.

Adds the project root to the import path and disables CSRF protection for the
test client (CSRF is verified on its own, not in every functional test).
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app  # noqa: E402

app.config["WTF_CSRF_ENABLED"] = False
