from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
import joblib
import os
import pandas as pd

class TopicModeler:
    def __init__(self, model_path="app/models/topic_model.pkl", vectorizer_path="app/models/vectorizer.pkl"):
        self.model_path = model_path
        self.vectorizer_path = vectorizer_path
        self.lda_model = None
        self.vectorizer = None
        self.n_topics = 3 # Respiratory, Digestive, Neurological/General as requested
        
        # Map topics to human readable names after inspection (Simplified assumption for this task)
        # In a real unsupervised scenario, we'd label these after training. 
        # Here we will try to guide it with a seeded dataset or just interpret result.
        self.topic_labels = {
            0: "Respiratory/General",
            1: "Digestive/Abdominal", 
            2: "Neurological/Pain"
        }

    def train(self, documents=None):
        """
        Train the LDA model. If documents not provided, use synthetic data.
        """
        if documents is None:
            # Synthetic medical documents
            documents = [
                # Respiratory
                "Coughing and shortness of breath", "Difficulty breathing and chest tightness", 
                "Wheezing and runny nose", "Sore throat and fever", "Lung congestion and mucus",
                # Digestive
                "Stomach pain and nausea", "Vomiting and diarrhea", "Abdominal cramps and bloating",
                "Acid reflux and heartburn", "Indigestion and stomach ache",
                # Neurological / Pain
                "Severe headache and dizziness", "Migraine and light sensitivity",
                "Numbness in fingers and toes", "Shooting pain in back", "Tremors and shaking hands"
            ] * 10 # Repeat to have enough data

        print("Training Topic Model...")
        self.vectorizer = CountVectorizer(stop_words='english', max_features=1000)
        dtm = self.vectorizer.fit_transform(documents)

        self.lda_model = LatentDirichletAllocation(n_components=self.n_topics, random_state=42)
        self.lda_model.fit(dtm)

        # Save
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.lda_model, self.model_path)
        joblib.dump(self.vectorizer, self.vectorizer_path)
        print("Topic Model saved.")

    def load_model(self):
        if os.path.exists(self.model_path) and os.path.exists(self.vectorizer_path):
            self.lda_model = joblib.load(self.model_path)
            self.vectorizer = joblib.load(self.vectorizer_path)
        else:
            self.train()

    def get_topic(self, text: str):
        if self.lda_model is None:
            self.load_model()
            
        vectorized_text = self.vectorizer.transform([text])
        topic_distribution = self.lda_model.transform(vectorized_text)[0]
        dominant_topic_idx = topic_distribution.argmax()
        
        return {
            "topic_id": int(dominant_topic_idx), # Cast to int for JSON serialization
            # "label": self.topic_labels.get(dominant_topic_idx, "Unknown"), # Labels might need tuning
            "confidence": round(topic_distribution[dominant_topic_idx], 2),
            "distribution": topic_distribution.tolist()
        }
