import requests
import time

BASE_URL = "http://localhost:8000/api/v1"
USER_ID = 999

def test_chat_appointment_flow():
    print("Testing Integrated Chat Appointment Flow...")
    
    # 1. Start booking via chat
    r1 = requests.post(f"{BASE_URL}/chat/", json={"user_id": USER_ID, "message": "I want to book an appointment"})
    print(f"Request 1: {r1.json()['response']}")
    assert "concern" in r1.json()['response'].lower()
    assert len(r1.json()['intent']['options']) > 0
    
    # 2. Provide problem
    r2 = requests.post(f"{BASE_URL}/chat/", json={"user_id": USER_ID, "message": "Fever"})
    print(f"Request 2: {r2.json()['response']}")
    assert "when would you like to come in" in r2.json()['response'].lower()
    
    # 3. Provide date
    r3 = requests.post(f"{BASE_URL}/chat/", json={"user_id": USER_ID, "message": "Tomorrow"})
    print(f"Request 3: {r3.json()['response']}")
    assert "what time" in r3.json()['response'].lower()
    assert "Morning" in r3.json()['intent']['options']

    # 4. Provide time
    r4 = requests.post(f"{BASE_URL}/chat/", json={"user_id": USER_ID, "message": "Morning"})
    print(f"Request 4: {r4.json()['response']}")
    assert "medical reports" in r4.json()['response'].lower()

    print("Success: Chat-based appointment flow verified!")

if __name__ == "__main__":
    try:
        test_chat_appointment_flow()
    except Exception as e:
        print(f"Test Failed: {e}")
