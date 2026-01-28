from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.services.appointment_flow import AppointmentBookingFlow

router = APIRouter(prefix="/appointments", tags=["appointments"])

from app.core.sessions import get_or_create_session, delete_session

class BookingRequest(BaseModel):
    user_id: int
    message: str

class BookingResponse(BaseModel):
    response: str
    state: str
    options: List[str] = []

@router.post("/process", response_model=BookingResponse)
async def process_booking(request: BookingRequest):
    user_id = request.user_id
    
    # Retrieve or create session via shared store
    flow = get_or_create_session(user_id)
    
    # Process input
    result = flow.process_input(request.message)
    
    # If completed, maybe save to DB and clear session
    if result['state'] == "COMPLETED":
        # Save to DB logic here
        # db.add(Appointment(...))
        # booking_sessions.pop(user_id) # Optional: keep for history
        pass
        
    return BookingResponse(
        response=result['response'],
        state=result['state'],
        options=result.get('options', [])
    )

@router.delete("/reset/{user_id}")
async def reset_booking(user_id: int):
    delete_session(user_id)
    return {"message": "Booking session reset"}
