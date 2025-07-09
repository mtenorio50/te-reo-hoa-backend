import pytest
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from main import app
from app.models import User

# This should match your TEST DB settings!
engine = create_engine("sqlite:///./test.db", future=True)
TestingSessionLocal = sessionmaker(
    bind=engine, autoflush=False, autocommit=False, future=True)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db

    from fastapi.testclient import TestClient
    return TestClient(app)


@pytest.fixture
def register_and_login_admin(client, db_session):
    # Use unique email to avoid conflicts
    unique_email = f"admin{uuid.uuid4().hex[:8]}@example.com"

    # Register admin user
    response = client.post("/users/register", json={
        "email": unique_email,
        "password": "adminpass"
    })
    assert response.status_code == 200
    user_id = response.json()["id"]

    # Promote to admin in DB
    user = db_session.query(User).filter_by(id=user_id).first()
    user.role = "admin"
    db_session.commit()

    # Login as admin
    login = client.post("/login/", data={
        "username": unique_email,
        "password": "adminpass"
    })
    assert login.status_code == 200
    return login.json()["access_token"]


@pytest.fixture
def register_and_login_learner(client):
    # Use unique email to avoid conflicts
    unique_email = f"learner{uuid.uuid4().hex[:8]}@example.com"

    response = client.post("/users/register", json={
        "email": unique_email,
        "password": "pass"
    })
    assert response.status_code == 200

    login = client.post("/login/", data={
        "username": unique_email,
        "password": "pass"
    })
    assert login.status_code == 200
    return login.json()["access_token"]


@pytest.fixture(autouse=True)
def mock_get_translation(monkeypatch):
    async def fake(word, max_retries=3):
        return {
            "candidates": [{
                "content": {"parts": [{
                    "text": '{"translation": "fake", "type": "noun", "domain": "", "example": "", "notes": ""}'
                }]}
            }]
        }
    monkeypatch.setattr("app.ai_integration.get_translation", fake)
