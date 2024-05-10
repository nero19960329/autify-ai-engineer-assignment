import os

if os.environ.get("ENV") == "test":
    os.environ["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
