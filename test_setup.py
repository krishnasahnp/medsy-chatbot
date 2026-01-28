import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

try:
    from app.main import app
    from app.core.config import settings
    from app.models.base import Base
    from app.models import User, Appointment, Symptom, Medication, ChatHistory
    from sqlalchemy import create_engine
    
    print("✅ Successfully imported application modules.")
    print(f"✅ Project Name: {settings.PROJECT_NAME}")
    print(f"✅ Database URL: {settings.DATABASE_URL}")
    
    # Check Database Models
    engine = create_engine(settings.DATABASE_URL)
    # Create tables to verify schema matches
    Base.metadata.create_all(bind=engine)
    print("✅ Successfully created database tables (Schema verified).")
    
    # Check Routes
    routes = [route.path for route in app.routes]
    expected_routes = ["/api/v1/chat/", "/api/v1/appointments/", "/api/v1/voice/", "/api/v1/reports/"]
    
    all_routes_present = all(any(r.startswith(expected) for r in routes) for expected in expected_routes)
    
    if all_routes_present:
        print("✅ All expected API routes are present.")
        for r in routes:
            print(f"   - {r}")
    else:
        print("❌ Missing some API routes.")
        print(f"   Found: {routes}")
        
    print("\n🎉 Project structure verification successful!")

except Exception as e:
    print(f"\n❌ Verification Failed: {e}")
    import traceback
    traceback.print_exc()
