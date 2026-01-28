from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean, Float, Text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./medsy.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    date_of_birth = Column(DateTime)
    gender = Column(String)
    emergency_contact = Column(String)
    insurance_info = Column(String)
    preferred_language = Column(String, default="en")
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    
    appointments = relationship("Appointment", back_populates="user")
    medical_records = relationship("Symptom", back_populates="user")
    medications = relationship("Medication", back_populates="user")
    chat_history = relationship("ChatHistory", back_populates="user")

class Appointment(Base):
    __tablename__ = "appointments"
    
    appointment_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    date = Column(DateTime)
    status = Column(String, default="Scheduled") # Scheduled, Completed, Cancelled
    problem_category = Column(String)
    description = Column(Text)
    doctor_name = Column(String)
    location = Column(String)
    
    user = relationship("User", back_populates="appointments")

class Symptom(Base):
    __tablename__ = "symptoms"
    
    symptom_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    symptom_name = Column(String)
    severity = Column(Integer) # 1-10
    start_date = Column(DateTime)
    frequency = Column(String)
    logged_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="medical_records")

class Medication(Base):
    __tablename__ = "medications"
    
    medication_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    name = Column(String)
    dosage = Column(String)
    frequency = Column(String)
    start_date = Column(DateTime)
    instructions = Column(String)
    adherence_rate = Column(Float, default=0.0)
    
    user = relationship("User", back_populates="medications")

class ChatHistory(Base):
    __tablename__ = "chat_history"
    
    message_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    message_text = Column(Text)
    sender = Column(String) # "user" or "bot"
    intent_detected = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="chat_history")

def init_db():
    Base.metadata.create_all(bind=engine)
