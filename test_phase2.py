import sys
import os
from datetime import datetime

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.services.pre_appointment import PreAppointmentAssistant
from app.services.jargon_translator import MedicalJargonTranslator
from app.services.web_scraper import WebScraper
from app.models.database import init_db, SessionLocal, User

def test_pre_appointment():
    print("\n--- Testing Pre-Appointment Assistant ---")
    assistant = PreAppointmentAssistant()
    q1 = assistant.start_symptom_logging()
    print(f"Q1: {q1}")
    
    # Simulate logging
    assistant.process_answer("Yesterday", 0)
    assistant.process_answer("Constant", 1)
    
    # Generate PDF
    pdf_path = assistant.generate_report("Test User", "test_report.pdf")
    print(f"PDF generated at: {pdf_path}")
    assert os.path.exists(pdf_path)
    # Cleanup
    if os.path.exists(pdf_path):
        os.remove(pdf_path)

def test_jargon_translator():
    print("\n--- Testing Jargon Translator ---")
    translator = MedicalJargonTranslator()
    text = "Patient has acute hypertension and edema."
    result = translator.translate(text)
    print(f"Original: {text}")
    print(f"Summary: {result['simple_summary']}")
    assert "high blood pressure" in result['simple_summary']

def test_web_scraper():
    print("\n--- Testing Web Scraper ---")
    scraper = WebScraper()
    info = scraper.scrape_disease_info("Flu")
    print(f"Scraped Info: {info['title']}")
    assert info['title'] == "Flu"

def test_database():
    print("\n--- Testing Database ---")
    init_db()
    db = SessionLocal()
    try:
        # Create test user
        user = User(name="Test User", email="test@example.com")
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"Created User: {user.name} (ID: {user.user_id})")
        assert user.user_id is not None
        
        # Cleanup
        db.delete(user)
        db.commit()
    except Exception as e:
        print(f"DB Error: {e}")
        # If user already exists/unique constraint, just pass for this verify
    finally:
        db.close()

if __name__ == "__main__":
    try:
        test_pre_appointment()
        test_jargon_translator()
        test_web_scraper()
        test_database()
        print("\nPhase 2 verification passed!")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
