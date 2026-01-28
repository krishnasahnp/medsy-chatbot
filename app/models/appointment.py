from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    doctor_name = Column(String, index=True)
    appointment_date = Column(DateTime, index=True)
    reason = Column(String)
    status = Column(String, default="scheduled") # scheduled, completed, cancelled

    owner = relationship("User", backref="appointments")
