import pytest
import sys
import os
from datetime import datetime

# Add root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.sentiment_analyzer import SentimentAnalyzer
from app.services.intent_classifier import IntentClassifier
from app.services.emergency_detector import EmergencyDetector
from app.services.medication_reminder import MedicationReminder

@pytest.fixture
def sentiment_analyzer():
    return SentimentAnalyzer()

@pytest.fixture
def intent_classifier():
    return IntentClassifier()

@pytest.fixture
def emergency_detector():
    return EmergencyDetector()

def test_sentiment_analysis(sentiment_analyzer):
    result = sentiment_analyzer.analyze("I am in severe pain, level 8")
    assert result['pain_level'] == 8
    assert result['anxiety_level'] > 0

def test_intent_classification(intent_classifier):
    # Ensure model is ready (might train on fly)
    result = intent_classifier.predict("Cancel my appointment")
    assert result['intent'] == "cancel_appointment"
    
def test_emergency_detection(emergency_detector):
    symptoms = ["chest pain", "shortness of breath", "sweating"]
    result = emergency_detector.check_symptoms(symptoms)
    assert result['is_emergency'] is True
    assert "Call Emergency Services" in result['action_required']

def test_medication_reminder():
    reminder = MedicationReminder()
    med_id = reminder.add_medication("u1", "Aspirin", "100mg", "daily", "Take with food")
    reminders = reminder.get_reminders_for_day("u1", datetime.now())
    assert len(reminders) == 1
    assert "Aspirin" in reminders[0]
