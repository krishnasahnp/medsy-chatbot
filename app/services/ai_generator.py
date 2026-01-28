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
        """Fallback responses for testing without API cost."""
        if "headache" in text.lower():
            return "I understand you have a headache. Have you been drinking enough water today? It might help to rest in a dark room."
        if sentiment and sentiment.get('is_panic'):
            return "Please try to take slow, deep breaths. I am here with you. If this is an emergency, please call 911."
        return f"I hear you saying '{text}'. Could you tell me more about that?"

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
