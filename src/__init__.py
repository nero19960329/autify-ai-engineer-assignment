"""
This module initializes the application and sets up the database connection.
It checks for the 'ENV' environment variable to determine the database URI.
"""

import os

if os.environ.get("ENV") == "test":
    os.environ["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
