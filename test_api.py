from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.main import app

client = TestClient(app)

def test_chat_endpoint():
    print("\n--- Testing Chat API ---")
    response = client.post("/api/v1/chat/", json={"user_id": 1, "message": "I have a headache"})
    print(f"Status: {response.status_code}")
    print(f"Data: {response.json()}")
    assert response.status_code == 200
    assert "headache" in response.json()['response'].lower() or "medicine" in response.json()['response'].lower()

def test_appointment_endpoint():
    print("\n--- Testing Appointment API ---")
    # 1. Initiate
    response = client.post("/api/v1/appointments/process", json={"user_id": 99, "message": "Book appointment"})
    print(f"Init: {response.json()}")
    assert response.json()['state'] == "PROBLEM_SELECTION"
    
    # 2. Select Problem
    response = client.post("/api/v1/appointments/process", json={"user_id": 99, "message": "Fever"})
    print(f"Problem: {response.json()}")
    assert response.json()['state'] == "DATE_SELECTION"

if __name__ == "__main__":
    try:
        test_chat_endpoint()
        test_appointment_endpoint()
        print("\nAPI Verification Passed!")
    except Exception as e:
        print(f"\nAPI Error: {e}")
