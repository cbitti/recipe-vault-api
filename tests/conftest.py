from typing import Generator
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.main import app
from app.db.session import get_db
from app.db.base import Base
from app.core.config import settings

# 1. Use a temporary SQLite DB for speed during tests
# Note: SQLite doesn't support ILIKE, so we'll have to be careful with search tests locally
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db() -> Generator:
    # Create the tables in the test DB
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    # Drop the tables after tests are done
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def client() -> Generator:
    # Dependency Override: Make the app use our Test DB instead of the Real DB
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session):
    """
    A helper fixture that registers a user, logs them in,
    and returns the authentication headers.
    """
    email = "test@example.com"
    password = "testpassword"

    # 1. Register
    client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json={"email": email, "password": password},
    )

    # 2. Login
    response = client.post(
        f"{settings.API_V1_STR}/auth/token",
        data={"username": email, "password": password},
    )
    auth_token = response.json()["access_token"]

    return {"Authorization": f"Bearer {auth_token}"}
