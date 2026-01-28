from datetime import datetime, timedelta

class MedicationReminder:
    def __init__(self):
        # Local storage for medication schedules (simulated DB)
        self.medications = {}
        
    def add_medication(self, user_id, med_name, dosage, frequency, instructions, start_date=None):
        """
        Add a medication to the schedule.
        frequency: "daily", "twice_daily", "every_other_day", "weekly"
        """
        if not start_date:
            start_date = datetime.now()
            
        med_id = f"MED-{len(self.medications)+1}"
        
        self.medications[med_id] = {
            "user_id": user_id,
            "name": med_name,
            "dosage": dosage,
            "frequency": frequency,
            "instructions": instructions, # e.g. "with food"
            "start_date": start_date,
            "history": []
        }
        return med_id

    def get_reminders_for_day(self, user_id, date: datetime):
        """
        Generate reminders for a specific day based on frequencies.
        Returns a list of reminder strings.
        """
        reminders = []
        for med_id, med in self.medications.items():
            if med["user_id"] != user_id:
                continue
                
            start = med["start_date"]
            delta_days = (date - start).days
            
            should_remind = False
            
            if med["frequency"] == "daily":
                should_remind = True
            elif med["frequency"] == "twice_daily":
                should_remind = True # Logic handled in timing
            elif med["frequency"] == "every_other_day":
                should_remind = (delta_days % 2 == 0)
            elif med["frequency"] == "weekly":
                should_remind = (delta_days % 7 == 0)
                
            if should_remind:
                # Add intelligent context
                context_msg = self._generate_context_message(med)
                reminders.append(context_msg)
                
        return reminders

    def _generate_context_message(self, med):
        """Generate a natural language reminder with instructions."""
        msg = f"Time to take {med['name']} ({med['dosage']})."
        
        if "food" in med["instructions"].lower():
            msg += " Please take it with a meal."
        elif "empty stomach" in med["instructions"].lower():
            msg += " Take it 30 mins before eating."
            
        if "dizzy" in med["instructions"].lower() or "drowsy" in med["instructions"].lower():
            msg += " Warning: May cause drowsiness."
            
        return msg

    def check_adherence(self, med_id):
        """Calculate simple adherence percentage."""
        med = self.medications.get(med_id)
        if not med or not med["history"]:
            return 0.0
            
        taken = sum(1 for entry in med["history"] if entry["status"] == "taken")
        total = len(med["history"])
        return round((taken / total) * 100, 1)

    def log_action(self, med_id, status="taken"):
        if med_id in self.medications:
            self.medications[med_id]["history"].append({
                "date": datetime.now(),
                "status": status
            })
