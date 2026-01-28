from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.sentiment_analyzer import SentimentAnalyzer
from app.services.intent_classifier import IntentClassifier
from app.services.ai_generator import AIGenerator
from app.services.emergency_detector import EmergencyDetector
from app.models.database import ChatHistory, SessionLocal
# from app.dependencies import get_db

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
    
    # 1. Emergency Check
    # (Simple logic: split tokens or pass full text as list for detector)
    emergency_status = emergency_detector.check_symptoms(message.split())
    if emergency_status['is_emergency']:
        return ChatResponse(
            response=emergency_status['alert_message'] + " " + emergency_status['action_required'],
            sentiment={},
            intent={"intent": "emergency_alert", "confidence": 1.0},
            is_emergency=True
        )

    # 2. Sentiment Analysis
    sentiment = sentiment_analyzer.analyze(message)
    
    # 3. Intent Classification
    intent = intent_classifier.predict(message)
    
    # 4. Generate AI Response
    # Context could be fetched from DB history
    response_text = ai_generator.generate_response(message, "No context yet", sentiment)
    
    # 5. Log to DB (Simplified)
    # db = SessionLocal()
    # db.add(ChatHistory(user_id=request.user_id, message_text=message, sender="user", intent_detected=intent['intent']))
    # db.add(ChatHistory(user_id=request.user_id, message_text=response_text, sender="bot"))
    # db.commit()
    # db.close()

    return ChatResponse(
        response=response_text,
        sentiment=sentiment,
        intent=intent,
        is_emergency=False
    )
