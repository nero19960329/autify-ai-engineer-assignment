from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database import get_db, SQLALCHEMY_DATABASE_URL
from src.models import Base
from src.app import app

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def connection():
    connection = engine.connect()
    yield connection
    connection.close()


@pytest.fixture(scope="function")
def db_session(connection):
    transaction = connection.begin()
    options = dict(bind=connection, binds={})
    session = TestingSessionLocal(**options)

    Base.metadata.create_all(bind=engine)

    yield session

    session.close()
    transaction.rollback()


@pytest.fixture(scope="function")
def client(request, db_session):
    dependency_overrides = getattr(
        request,
        "param",
        {},
    )

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    dependency_overrides[get_db] = override_get_db
    app.dependency_overrides.update(dependency_overrides)

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
