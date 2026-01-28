import re
from functools import lru_cache

class MedicalJargonTranslator:
    def __init__(self):
        self.dictionary = {
            "hypertension": "High blood pressure",
            "acute": "Sudden, recent onset",
            "chronic": "Long-lasting condition, continuing for a long time",
            "benign": "Not harmful or cancerous",
            "malignant": "Harmful, likely cancerous",
            "edema": "Swelling caused by fluid trapped in your body's tissues",
            "idiopathic": "Of unknown cause",
            "myocardial infarction": "Heart attack",
            "cerebrovascular accident": "Stroke",
            "dyspnea": "Shortness of breath or difficulty breathing",
            "bradycardia": "Slower than normal heart rate",
            "tachycardia": "Faster than normal heart rate",
            "analgesic": "Pain reliever",
            "anti-inflammatory": "Reduces swelling and inflammation",
            "biopsy": "Removal of a small piece of tissue for examination",
            "prognosis": "The likely outcome or course of a disease",
            "remission": "A decrease in or disappearance of signs and symptoms of disease",
            "metastasis": "Spread of cancer cells to new areas of the body",
            "intravenous": "Delivered directly into a vein",
            "subcutaneous": "Under the skin"
        }

    @lru_cache(maxsize=256)
    def translate(self, text: str) -> dict:
        """
        Identify medical terms in text and provide simpler explanations.
        """
        simplified_text = text
        terms_found = []
        
        # Simple case-insensitive replacement/matching
        for term, explanation in self.dictionary.items():
            pattern = re.compile(re.escape(term), re.IGNORECASE)
            if pattern.search(text):
                terms_found.append({
                    "term": term,
                    "explanation": explanation
                })
                # Create simplistic "Explain like I'm 5" version inline?
                # For now just identifying terms.
                
        return {
            "original_text": text,
            "terms_identified": terms_found,
            "simple_summary": self._generate_summary(text, terms_found)
        }

    def _generate_summary(self, text, terms):
        if not terms:
            return "No complex terminology detected."
        
        parts = []
        for term in terms:
            parts.append(f"'{term['term']}' means {term['explanation'].lower()}")
            
        return "In simple terms: " + "; ".join(parts) + "."

class TreatmentPlanGenerator:
    def __init__(self):
        pass

    def generate_plan(self, prescription_text):
        """
        Parse simple prescription text and generate a schedule.
        (Simplified parsing for this task)
        """
        # Example input: "Take Amoxicillin 500mg once daily for 7 days"
        plan = {
            "medications": [],
            "schedule": [],
            "warnings": []
        }
        
        # Mock logic similar to what we'd do with named entity recognition
        if "Amoxicillin" in prescription_text:
            plan["medications"].append({
                "name": "Amoxicillin",
                "purpose": "Antibiotic to treat bacterial infection",
                "instructions": "Take with food to avoid stomach upset"
            })
            plan["schedule"].append("Morning (Breakfast)")
            plan["warnings"].append("Finish the full course even if you feel better.")

        return plan
