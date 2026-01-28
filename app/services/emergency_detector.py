from datetime import datetime

class EmergencyDetector:
    def __init__(self):
        # Critical patterns mapping symptoms to potential conditions and severity
        # Format: {condition: {symptoms: [], threshold_score: int}}
        self.rules = {
            "Possible Heart Attack": {
                "symptoms": ["chest pain", "shortness of breath", "sweating", "nausea", "arm pain"],
                "required_count": 2,
                "severity_base": 10
            },
            "Possible Stroke": {
                "symptoms": ["severe headache", "vision changes", "confusion", "numbness", "slurred speech"],
                "required_count": 2,
                "severity_base": 10
            },
            "Possible Meningitis": {
                "symptoms": ["high fever", "stiff neck", "sensitivity to light", "severe headache"],
                "required_count": 2,
                "severity_base": 9
            },
            "Severe Allergic Reaction": {
                "symptoms": ["difficulty breathing", "wheezing", "swelling", "hives"],
                "required_count": 2,
                "severity_base": 9
            },
            "Possible Appendicitis": {
                "symptoms": ["severe abdominal pain", "vomiting", "fever", "loss of appetite"],
                "required_count": 3,
                "severity_base": 8
            }
        }
        
        # Base severity scores for individual symptoms
        self.symptom_scores = {
            "chest pain": 8, "shortness of breath": 7, "unconscious": 10,
            "severe headache": 6, "vision changes": 6, "difficulty breathing": 9,
            "bleeding": 7, "high fever": 5, "seizure": 10
        }

    def check_symptoms(self, user_symptoms: list) -> dict:
        """
        Analyze a list of symptoms string for emergency conditions.
        Returns a dict with alert status and details.
        """
        user_symptoms = [s.lower() for s in user_symptoms]
        detected_conditions = []
        max_severity = 0
        
        # Rule-based check
        for condition, criteria in self.rules.items():
            match_count = 0
            for crit_symptom in criteria["symptoms"]:
                # Fuzzy match logic (simplified)
                if any(crit_symptom in s for s in user_symptoms):
                    match_count += 1
            
            if match_count >= criteria["required_count"]:
                detected_conditions.append(condition)
                max_severity = max(max_severity, criteria["severity_base"])

        # Individual severe symptom check
        for symptom, score in self.symptom_scores.items():
            if any(symptom in s for s in user_symptoms):
                max_severity = max(max_severity, score)
                if score >= 9:
                    detected_conditions.append(f"Critical Symptom: {symptom}")

        is_emergency = max_severity >= 8 or len(detected_conditions) > 0
        
        response = {
            "is_emergency": is_emergency,
            "severity_score": max_severity,
            "conditions_detected": list(set(detected_conditions)),
            "alert_message": "",
            "action_required": "None"
        }
        
        if is_emergency:
            response["alert_message"] = "⚠️ URGENT: Potential Emergency Detected. Please seek immediate medical attention."
            response["action_required"] = "Call Emergency Services (911) or go to the nearest ER."
        
        return response
