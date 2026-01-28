import os
# from openai import OpenAI # Uncomment in production

class AIGenerator:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        # self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def generate_response(self, user_text, context, sentiment=None):
        """
        Generate an empathetic response using LLM.
        """
        # Prompt engineering
        system_prompt = (
            "You are Medsy, an empathetic and professional medical assistant. "
            "Your goal is to help patients feel calm and understood. "
            "Keep responses concise (under 50 words) unless explaining a complex topic."
        )
        
        if sentiment and sentiment.get('anxiety_level', 0) > 5:
            system_prompt += " The user seems anxious. Be extra reassuring."

        # Mock response if no API key
        if not self.api_key:
            return self._mock_response(user_text, sentiment)

        try:
            # response = self.client.chat.completions.create(
            #     model="gpt-4o",
            #     messages=[
            #         {"role": "system", "content": system_prompt},
            #         {"role": "user", "content": f"Context: {context}\nUser: {user_text}"}
            #     ]
            # )
            # return response.choices[0].message.content
            return self._mock_response(user_text, sentiment) # Fallback
            
        except Exception as e:
            print(f"AI Generation Error: {e}")
            return "I apologize, I'm having trouble connecting to my brain right now. How else can I help?"

    def _mock_response(self, text, sentiment):
        """Robust keyword-based response system for high-quality fallback."""
        text = text.lower()
        
        # 1. Greetings & Meta
        if any(w in text for w in ["hello", "hi", "hey", "greetings"]):
            return "Hello! I'm Medsy, your medical companion. How can I help you today? I can help with symptom checking, booking appointments, or medication info."
        
        if any(w in text for w in ["who are you", "what can you do", "help", "guide"]):
            return ("I am Medsy, an AI-powered health assistant. You can ask me about:\n"
                    "• Common symptoms (cough, fever, etc.)\n"
                    "• Booking medical appointments\n"
                    "• Understanding your medications\n"
                    "• Emergency detection")

        # 2. Symptom Deep-Dive
        if any(w in text for w in ["cold", "cough", "flu", "sneeze"]):
            return ("It sounds like you might be dealing with a viral infection. Common symptoms include coughing, congestion, and a sore throat. "
                    "Most viral colds resolve on their own with rest and fluids. Would you like to book a checkup to be sure?")
        
        if any(w in text for w in ["fever", "temp", "hot", "shiver"]):
            return ("A fever is usually a sign of your immune system fighting an infection. For adults, a high fever is generally above 103°F (39.4°C). "
                    "Make sure to stay hydrated. If the fever persists for more than 3 days, please schedule a visit.")

        if any(w in text for w in ["pain", "hurt", "ache"]):
            if "chest" in text:
                return "URGENT: Since you mentioned chest pain, please sit down and rest. If it's severe or radiating, call emergency services immediately."
            return "I'm sorry you're in pain. For minor aches, rest and over-the-counter relief can help, but recurring pain should be examined by a professional."

        # 3. Medications
        if any(w in text for w in ["medicine", "pill", "drug", "tablet", "dosage"]):
            return ("Medication should always be taken exactly as prescribed by your doctor. "
                    "Would you like me to look up information on a specific drug like Paracetamol or Ibuprofen?")

        # 4. Appointments
        if any(w in text for w in ["appointment", "book", "see a doctor", "visit"]):
            return "I can certainly help you with that! Just say 'I want to book an appointment' and I'll start the scheduling process for you."

        # 5. Default "Help Menu" Fallback (Proper Fix for repetition)
        return ("I'm not exactly sure how to help with that yet. You can try asking:\n"
                "• 'What are cold symptoms?'\n"
                "• 'I want to book an appointment'\n"
                "• 'I have a fever'\n"
                "• 'Tell me about medications'")

    def generate_symptom_report(self, symptom_log):
        """
        Convert raw log to professional summary.
        """
        # In production this would send the JSON log to GPT
        return f"Patient reports symptoms starting on {symptom_log[0]['timestamp']}. Primary complaints include..."

    def simplify_jargon_ai(self, text):
        """
        Use AI to explain complex text if dictionary fails.
        """
        return f"[AI Explanation of: {text}]"
