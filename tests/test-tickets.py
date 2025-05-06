import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import SessionLocal, engine
from app.models import ticket, message, user

client = TestClient(app)

@pytest.fixture
def db_session():
    ticket.Base.metadata.create_all(bind=engine)
    message.Base.metadata.create_all(bind=engine)
    user.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()

@pytest.fixture
def user_data():
    return {"name": "Test User", "email": "test@example.com"}

@pytest.fixture
def ticket_data():
    return {"title": "Test Ticket", "description": "Test Description", "user_id": 1}

@pytest.fixture
def message_data():
    return {"content": "Test Message", "user_id": 1, "parent_message_id": None}

def test_create_ticket(ticket_data):
    response = client.post("/users/", json=user_data())
    response = client.post("/tickets/", json=ticket_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Ticket"
    assert response.json()["status"] == "open"

def test_get_ticket():
    response = client.post("/users/", json=user_data())
    response = client.post("/tickets/", json=ticket_data())
    ticket_id = response.json()["id"]
    response = client.get(f"/tickets/{ticket_id}")
    assert response.status_code == 200
    assert response.json()["id"] == ticket_id
    assert "messages" in response.json()

def test_update_ticket_status():
    response = client.post("/users/", json=user_data())
    response = client.post("/tickets/", json=ticket_data())
    ticket_id = response.json()["id"]
    response = client.patch(f"/tickets/{ticket_id}", json={"status": "in_progress"})
    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"

def test_get_tickets_with_filter():
    response = client.post("/users/", json=user_data())
    response = client.post("/tickets/", json=ticket_data())
    response = client.get("/tickets/?status=open&user_id=1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_create_message(message_data):
    response = client.post("/users/", json=user_data())
    response = client.post("/tickets/", json=ticket_data())
    ticket_id = response.json()["id"]
    response = client.post(f"/tickets/{ticket_id}/messages/", json=message_data)
    assert response.status_code == 200
    assert response.json()["content"] == "Test Message"
    assert response.json()["ticket_id"] == ticket_id

def test_create_child_message():
    response = client.post("/users/", json=user_data())
    response = client.post("/tickets/", json=ticket_data())
    ticket_id = response.json()["id"]
    parent = client.post(f"/tickets/{ticket_id}/messages/", json={"content": "Parent Message", "user_id": 1})
    parent_id = parent.json()["id"]
    response = client.post(f"/tickets/{ticket_id}/messages/", json={"content": "Child Message", "user_id": 1, "parent_message_id": parent_id})
    assert response.status_code == 200
    assert response.json()["parent_message_id"] == parent_id

def test_create_message_invalid_parent():
    response = client.post("/users/", json=user_data())
    response = client.post("/tickets/", json=ticket_data())
    ticket_id = response.json()["id"]
    response = client.post(f"/tickets/{ticket_id}/messages/", json={"content": "Invalid Parent", "user_id": 1, "parent_message_id": 999})
    assert response.status_code == 400
    assert response.json()["detail"] == "Parent message not found or does not belong to this ticket"

def test_get_nonexistent_ticket():
    response = client.get("/tickets/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Ticket not found"