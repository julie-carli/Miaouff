"""WSGI entry point.

Render and gunicorn import the `app` object from this module (`app:app`).
The actual application is assembled by the factory in ``factory.py``.
"""

import os

from factory import create_app

app = create_app()

if __name__ == "__main__":
    # debug=True is for local development only, never use in production.
    app.run(debug=os.environ.get("FLASK_DEBUG", "False") == "True")
