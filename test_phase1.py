import sys
import os
from datetime import datetime, timedelta

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.services.appointment_flow import AppointmentBookingFlow
from app.services.emergency_detector import EmergencyDetector
from app.services.medication_reminder import MedicationReminder
# from app.services.voice_handler import VoiceHandler # Skipped due to audio dependency in headless env

def test_appointment_flow():
    print("\n--- Testing Appointment Flow ---")
    flow = AppointmentBookingFlow()
    
    # Simulate conversation
    print(f"State: {flow.state}")
    res = flow.process_input("Book appointment")
    print(f"Bot: {res['response']}")
    
    res = flow.process_input("I have a severe headache")
    print(f"User: Headache -> Bot: {res['response']}")
    
    res = flow.process_input("Next Monday")
    print(f"User: Next Monday -> Bot: {res['response']}")
    
    res = flow.process_input("Morning")
    print(f"User: Morning -> Bot: {res['response']}")
    
    res = flow.process_input("No")
    print(f"User: No files -> Bot: {res['response']}")
    
    print(f"Final Data: {flow.booking_data}")
    assert flow.state == "COMPLETED"

def test_emergency_detector():
    print("\n--- Testing Emergency Detector ---")
    detector = EmergencyDetector()
    
    # Case 1: Heart Attack symptoms
    symptoms = ["chest pain", "shortness of breath", "sweating"]
    res = detector.check_symptoms(symptoms)
    print(f"Symptoms: {symptoms}")
    print(f"Emergency: {res['is_emergency']} (Alert: {res['alert_message']})")
    assert res['is_emergency'] is True

    # Case 2: Mild cold
    symptoms = ["runny nose", "sneezing"]
    res = detector.check_symptoms(symptoms)
    print(f"Symptoms: {symptoms}")
    print(f"Emergency: {res['is_emergency']}")
    assert res['is_emergency'] is False

def test_medication_reminder():
    print("\n--- Testing Medication Reminder ---")
    reminder = MedicationReminder()
    
    reminder.add_medication("user1", "Lisinopril", "10mg", "daily", "Take with food")
    
    reminders = reminder.get_reminders_for_day("user1", datetime.now())
    print(f"Reminders Today: {reminders}")
    assert len(reminders) > 0
    assert "meal" in reminders[0]

if __name__ == "__main__":
    try:
        test_appointment_flow()
        test_emergency_detector()
        test_medication_reminder()
        print("\nPhase 1 verification passed!")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
