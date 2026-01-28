import re
import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class MedicalNLPProcessor:
    def __init__(self):
        # Ensure NLTK data is downloaded
        self._download_nltk_resources()
        
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
        # Medical Knowledge Base (Simplified for Demo)
        self.common_symptoms = [
            "headache", "fever", "cough", "nausea", "vomiting", "fatigue", 
            "dizziness", "chest pain", "back pain", "stomach ache", "rash",
            "shortness of breath", "sore throat", "chills", "sweating"
        ]
        
        self.urgency_keywords = [
            "severe", "emergency", "bleeding", "chest pain", "heart attack",
            "stroke", "unconscious", "difficulty breathing", "broken", "critical"
        ]
        
        self.intent_keywords = {
            "book_appointment": ["book", "schedule", "appointment", "reserve", "meet"],
            "cancel_appointment": ["cancel", "delete", "remove appointment"],
            "reschedule_appointment": ["reschedule", "change time", "move appointment"],
            "symptom_check": ["check", "symptom", "diagnosis", "feel", "pain"],
        }

        # Initialize Vectorizer for Similarity
        self.vectorizer = TfidfVectorizer()
        self._fit_vectorizers()

    def _download_nltk_resources(self):
        """Download necessary NLTK data if not present."""
        resources = ['punkt', 'wordnet', 'stopwords', 'omw-1.4', 'punkt_tab']
        for res in resources:
            try:
                nltk.data.find(f'tokenizers/{res}')
            except LookupError:
                try:
                    nltk.data.find(f'corpora/{res}')
                except LookupError:
                    nltk.download(res, quiet=True)

    def _fit_vectorizers(self):
        """Fit TF-IDF vectorizer on the known symptoms list."""
        self.tfidf_matrix = self.vectorizer.fit_transform(self.common_symptoms)

    # --- 1. REGEX PATTERNS ---
    def extract_entities(self, text: str) -> dict:
        """Extract patterns using Regex."""
        entities = {
            "email": None,
            "phone": None,
            "date": None,
            "potential_symptoms": []
        }
        
        # Email Pattern
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        email_match = re.search(email_pattern, text)
        if email_match:
            entities["email"] = email_match.group(0)

        # Phone Pattern (Generic)
        phone_pattern = r'(\+\d{1,3}[-.]?)?\(?\d{3}\)?[-.]?\d{3}[-.]?\d{4}'
        phone_match = re.search(phone_pattern, text)
        if phone_match:
            entities["phone"] = phone_match.group(0)

        # Date Pattern (simple DD/MM/YYYY or DD-MM-YYYY)
        date_pattern = r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'
        date_match = re.search(date_pattern, text)
        if date_match:
            entities["date"] = date_match.group(0)

        # Basic Symptom Regex (Regex for pain/painful variants)
        pain_pattern = r'\b(\w+)\s+(pain|ache|hurt|sore)\b'
        pain_matches = re.findall(pain_pattern, text, re.IGNORECASE)
        for pm in pain_matches:
            entities["potential_symptoms"].append(f"{pm[0]} {pm[1]}")

        return entities

    # --- 2. STEMMING & LEMMATIZATION ---
    def preprocess_text(self, text: str) -> dict:
        """Tokenize and normalize text."""
        # Clean text
        text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
        tokens = word_tokenize(text)
        
        filtered_tokens = [w for w in tokens if w not in self.stop_words]
        
        stemmed = [self.stemmer.stem(w) for w in filtered_tokens]
        lemmatized = [self.lemmatizer.lemmatize(w) for w in filtered_tokens]
        
        return {
            "tokens": tokens,
            "filtered": filtered_tokens,
            "stemmed": stemmed,
            "lemmatized": lemmatized
        }

    # --- 3. KEYWORD DETECTION ---
    def detect_intent(self, text: str) -> str:
        """Determine user intent based on keywords."""
        text_lower = text.lower()
        
        # Check against intent dictionary
        for intent, keywords in self.intent_keywords.items():
            for kw in keywords:
                if kw in text_lower:
                    return intent
        return "general_chat"

    def assess_urgency(self, text: str) -> dict:
        """Check for urgency keywords."""
        text_lower = text.lower()
        detected_urgency = []
        
        for kw in self.urgency_keywords:
            if kw in text_lower:
                detected_urgency.append(kw)
        
        is_urgent = len(detected_urgency) > 0
        return {
            "is_urgent": is_urgent,
            "flags": detected_urgency,
            "advice": "Please call emergency services immediately." if is_urgent else "Standard priority."
        }
    
    def extract_known_symptoms(self, text: str) -> list:
        """Exact keyword matching for known symptoms list."""
        found = []
        text_lower = text.lower()
        for symptom in self.common_symptoms:
            if symptom in text_lower:
                found.append(symptom)
        return found

    # --- 4. BAG-OF-WORDS & TF-IDF ---
    def find_similar_symptom(self, query: str) -> dict:
        """Find the most similar known symptom using TF-IDF."""
        # Transform query
        query_vec = self.vectorizer.transform([query])
        
        # Calculate cosine similarity with all known symptoms
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        
        # Get best match
        best_idx = np.argmax(similarities)
        best_score = similarities[best_idx]
        
        if best_score > 0.2: # Threshold
            return {
                "match": self.common_symptoms[best_idx],
                "score": float(best_score)
            }
        return {"match": None, "score": 0.0}

if __name__ == "__main__":
    # Simple manual test when running module directly
    nlp = MedicalNLPProcessor()
    
    test_text = "I have a severe headache and high fever. Can I book an appointment for 12/05/2024?"
    print(f"Text: {test_text}")
    print(f"Entities: {nlp.extract_entities(test_text)}")
    print(f"Intent: {nlp.detect_intent(test_text)}")
    print(f"Urgency: {nlp.assess_urgency(test_text)}")
    print(f"Symptoms (Keyword): {nlp.extract_known_symptoms(test_text)}")
    print(f"Similarity ('head pain'): {nlp.find_similar_symptom('head pain')}")
