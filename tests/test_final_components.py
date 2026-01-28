import pytest
from unittest.mock import MagicMock, patch
import sys
import os
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.alert_system import AlertSystem
from app.services.medication_reminder import MedicationReminder
from app.services.voice_handler import VoiceHandler

# --- Alert System Tests ---
def test_alert_system_trigger():
    alert = AlertSystem()
    # Mock the internal send methods to avoid spam/errors
    alert._send_sms = MagicMock()
    alert._send_email = MagicMock()
    
    result = alert.trigger_alert("Test User", "Heart Attack", "Home")
    
    assert result['status'] == "success"
    assert len(alert.notification_log) == 1
    assert alert.notification_log[0]['condition'] == "Heart Attack"
    alert._send_sms.assert_called_once()
    alert._send_email.assert_called_once()

# --- Medication Adherence Tests ---
def test_adherence_calculation():
    reminder = MedicationReminder()
    med_id = reminder.add_medication("u1", "Pill X", "10mg", "daily", "None")
    
    # Initially 0
    assert reminder.check_adherence(med_id) == 0.0
    
    # Log some actions
    reminder.log_action(med_id, "taken")
    reminder.log_action(med_id, "missed")
    reminder.log_action(med_id, "taken")
    reminder.log_action(med_id, "taken")
    # Total 4, Taken 3 => 75%
    
    assert reminder.check_adherence(med_id) == 75.0

# --- Voice Handler Tests (Mocked) ---
def test_voice_speak():
    # Mock pyttsx3 to avoid audio device errors in headless env
    with patch('app.services.voice_handler.pyttsx3.init') as mock_init:
        mock_engine = MagicMock()
        mock_init.return_value = mock_engine
        
        handler = VoiceHandler()
        handler.speak("Hello")
        
        mock_engine.say.assert_called_with("Hello")
        mock_engine.runAndWait.assert_called_once()

def test_voice_listen_mock():
    # Mock SpeechRecognition
    with patch('app.services.voice_handler.sr.Microphone') as mock_mic, \
         patch('app.services.voice_handler.sr.Recognizer') as mock_rec:
        
        mock_recognizer = mock_rec.return_value
        # Mock recognize_google to return "Hello Medsy"
        mock_recognizer.listen.return_value = "audio_data"
        mock_recognizer.recognize_google.return_value = "Hello Medsy"
        
        handler = VoiceHandler()
        text = handler.listen()
        
        assert text == "hello medsy"
