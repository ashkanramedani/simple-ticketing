import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import SessionLocal, engine
from app.models import user

client = TestClient(app)

@pytest.fixture
def db_session():
    user.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()

@pytest.fixture
def user_data():
    return {"name": "Test User", "email": "test@example.com"}

def test_create_user(user_data):
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

def test_create_duplicate_user(user_data):
    client.post("/users/", json=user_data)
    response = client.post("/users/", json=user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already exists"

def test_create_user_invalid_email():
    invalid_user = {"name": "Invalid User", "email": "invalid"}
    response = client.post("/users/", json=invalid_user)
    assert response.status_code == 422
    assert "value is not a valid email address" in str(response.json())