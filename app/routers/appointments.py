from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.services.appointment_flow import AppointmentBookingFlow

router = APIRouter(prefix="/appointments", tags=["appointments"])

# In-memory session store for demo purposes (production would use Redis/DB)
booking_sessions = {} 

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
    
    # Retrieve or create session
    if user_id not in booking_sessions:
        booking_sessions[user_id] = AppointmentBookingFlow()
        
    flow = booking_sessions[user_id]
    
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
    if user_id in booking_sessions:
        booking_sessions.pop(user_id)
    return {"message": "Booking session reset"}
