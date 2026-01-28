from app.services.appointment_flow import AppointmentBookingFlow

# In-memory session store for tracking appointment flows across multiple routers
# Key: user_id (int), Value: AppointmentBookingFlow instance
booking_sessions = {}

def get_or_create_session(user_id: int) -> AppointmentBookingFlow:
    if user_id not in booking_sessions:
        booking_sessions[user_id] = AppointmentBookingFlow()
    return booking_sessions[user_id]

def delete_session(user_id: int):
    if user_id in booking_sessions:
        booking_sessions.pop(user_id)
