import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from .. import config
from ..database import Base, get_db
from ..main import app

SQLALCHEMY_DATABASE_URL = (
        f"postgresql+psycopg://"
        f"{config.USER}:{config.PASSWORD}@"
        f"{config.HOST}:{config.PORT}/{config.TESTDB}"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
