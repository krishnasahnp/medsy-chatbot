import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Med Companion API"}

def test_chat_interaction():
    response = client.post("/api/v1/chat/", json={"user_id": 1, "message": "Hello Medsy"})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "sentiment" in data

def test_appointment_booking_flow():
    # 1. Start booking
    response = client.post("/api/v1/appointments/process", json={"user_id": 123, "message": "Book appointment"})
    assert response.status_code == 200
    assert response.json()['state'] == "PROBLEM_SELECTION"
    
    # 2. Provide problem
    response = client.post("/api/v1/appointments/process", json={"user_id": 123, "message": "Headache"})
    assert response.json()['state'] == "DATE_SELECTION"
