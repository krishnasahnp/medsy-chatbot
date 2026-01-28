from datetime import datetime, timedelta
import random

class AppointmentBookingFlow:
    # States
    INITIATE = "INITIATE"
    PROBLEM_SELECTION = "PROBLEM_SELECTION"
    DATE_SELECTION = "DATE_SELECTION"
    TIME_SELECTION = "TIME_SELECTION"
    FILE_UPLOAD = "FILE_UPLOAD"
    CONFIRMATION = "CONFIRMATION"
    COMPLETED = "COMPLETED"

    def __init__(self):
        self.state = self.INITIATE
        self.booking_data = {
            "problem": None,
            "date": None,
            "time": None,
            "files": [],
            "id": None
        }
        self.common_problems = [
            "General checkup", "Fever/Cold", "Headache/Migraine", 
            "Stomach pain", "Chest pain", "Skin problems", 
            "Joint/Muscle pain", "Allergies", "Diabetes check", 
            "BP Check", "Women's health", "Mental health", 
            "Injury", "Follow-up", "Other"
        ]

    def process_input(self, user_input: str) -> dict:
        """
        Process user input based on current state.
        Returns a dict with 'response' (str) and 'options' (list, optional).
        """
        response = ""
        options = []
        
        # Simple state machine logic
        if self.state == self.INITIATE:
            self.state = self.PROBLEM_SELECTION
            response = "I'll help you book an appointment. Let's start with your main concern. Please choose from the list or say it."
            options = self.common_problems
            
        elif self.state == self.PROBLEM_SELECTION:
            # Simple matching or fallback
            selection = self._match_problem(user_input)
            self.booking_data["problem"] = selection
            self.state = self.DATE_SELECTION
            response = f"Okay, checking for {selection}. When would you like to come in? (e.g., Next Monday, Jan 30th)"
            
        elif self.state == self.DATE_SELECTION:
            # In a real app, use dateparser logic
            self.booking_data["date"] = user_input # Placeholder
            self.state = self.TIME_SELECTION
            response = f"Got it, {user_input}. What time works best? We have slots in Morning, Afternoon, or Evening."
            options = ["Morning", "Afternoon", "Evening"]
            
        elif self.state == self.TIME_SELECTION:
            self.booking_data["time"] = user_input
            self.state = self.FILE_UPLOAD
            response = "Noted. Do you have any medical reports or files to share? (Yes/No)"
            
        elif self.state == self.FILE_UPLOAD:
            if "yes" in user_input.lower():
                response = "Please upload your files using the interface. (Simulated: File received). Proceeding to confirmation."
            else:
                response = "Okay, no files. Let's review."
            
            self.state = self.CONFIRMATION
            return self.process_input("") # Auto-transition to confirmation msg
            
        elif self.state == self.CONFIRMATION:
            self.booking_data["id"] = f"APT-{random.randint(1000,9999)}"
            summary = (
                f"Appointment Confirmed!\n"
                f"ID: {self.booking_data['id']}\n"
                f"Problem: {self.booking_data['problem']}\n"
                f"Date: {self.booking_data['date']}\n"
                f"Time: {self.booking_data['time']}"
            )
            response = summary
            self.state = self.COMPLETED
            
        elif self.state == self.COMPLETED:
            response = "Your appointment is already booked. Do you need anything else?"
            
        return {
            "response": response,
            "options": options,
            "state": self.state,
            "data": self.booking_data
        }

    def _match_problem(self, input_text):
        """Simple fuzzy match attempt or return input"""
        input_text = input_text.lower()
        for prob in self.common_problems:
            if prob.lower() in input_text:
                return prob
            # Handle numeric selection "number 1" or "option 1"
            # (Simplification: assuming user says text for now)
        return input_text.capitalize()

    def reset(self):
        self.__init__()
