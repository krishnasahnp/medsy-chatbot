from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.sentiment_analyzer import SentimentAnalyzer
from app.services.intent_classifier import IntentClassifier
from app.services.ai_generator import AIGenerator
from app.services.emergency_detector import EmergencyDetector
from app.core.sessions import get_or_create_session, delete_session, booking_sessions
from app.services.appointment_flow import AppointmentBookingFlow

router = APIRouter(prefix="/chat", tags=["chat"])

# Initialize services
sentiment_analyzer = SentimentAnalyzer()
intent_classifier = IntentClassifier()
ai_generator = AIGenerator()
emergency_detector = EmergencyDetector()

class ChatRequest(BaseModel):
    user_id: Optional[int] = 1
    message: str

class ChatResponse(BaseModel):
    response: str
    sentiment: dict
    intent: dict
    is_emergency: bool

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    message = request.message
    user_id = request.user_id
    
    # 1. Emergency Check
    emergency_status = emergency_detector.check_symptoms(message.split())
    if emergency_status['is_emergency']:
        return ChatResponse(
            response=emergency_status['alert_message'] + " " + emergency_status['action_required'],
            sentiment={},
            intent={"intent": "emergency_alert", "confidence": 1.0},
            is_emergency=True
        )

    # 2. Appointment Flow Check
    # If the user is already in a session OR the intent is to book
    intent = intent_classifier.predict(message)
    
    if user_id in booking_sessions or intent['intent'] == "book_appointment":
        flow = get_or_create_session(user_id)
        
        # If the session was already completed, and user is NOT trying to book again,
        # clear it so they can go back to general chat.
        if flow.state == AppointmentBookingFlow.COMPLETED and intent['intent'] != "book_appointment":
            delete_session(user_id)
        else:
            result = flow.process_input(message)
            response_text = result['response']
            intent['options'] = result.get('options', [])
            intent['state'] = result.get('state')
            
            return ChatResponse(
                response=response_text,
                sentiment=sentiment_analyzer.analyze(message),
                intent=intent,
                is_emergency=False
            )

    # 3. Standard Sentiment Analysis
    sentiment = sentiment_analyzer.analyze(message)
    
    # 4. Generate AI Response for general queries
    response_text = ai_generator.generate_response(message, "No context yet", sentiment)
    
    return ChatResponse(
        response=response_text,
        sentiment=sentiment,
        intent=intent,
        is_emergency=False
    )
