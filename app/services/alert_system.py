import time

class AlertSystem:
    def __init__(self):
        self.notification_log = []

    def trigger_alert(self, user_name, condition, location="Unknown"):
        """
        Simulate triggering an emergency alert to contacts/authorities.
        """
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        alert_msg = f"[{timestamp}] EMERGENCY ALERT: User {user_name} at {location} showing signs of {condition}. Contacts notified."
        
        # Simulate SMS/Email API call
        self._send_sms("Emergency Contact", alert_msg)
        self._send_email("doctor@medsy.com", f"URGENT: {user_name}", alert_msg)
        
        self.notification_log.append({
            "timestamp": timestamp,
            "user": user_name,
            "condition": condition,
            "status": "SENT"
        })
        
        return {
            "status": "success",
            "message": "Emergency protocols initiated. Contacts notified.",
            "timestamp": timestamp
        }

    def _send_sms(self, recipient, message):
        print(f"Sending SMS to {recipient}: {message}")

    def _send_email(self, recipient, subject, body):
        print(f"Sending Email to {recipient} | Subject: {subject} | Body: {body}")

if __name__ == "__main__":
    alert = AlertSystem()
    print(alert.trigger_alert("John Doe", "Heart Attack"))
