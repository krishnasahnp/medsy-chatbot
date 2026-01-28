import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
from functools import lru_cache

# Download VADER lexicon if not already present
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

class SentimentAnalyzer:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        self.panic_keywords = [
            "emergency", "severe", "can't breathe", "dying", "help", 
            "unbearable", "crushing", "stroke", "heart attack", "bleeding"
        ]

    @lru_cache(maxsize=128)
    def analyze(self, text: str) -> dict:
        """
        Analyze the text for sentiment, anxiety, panic, and pain.
        """
        scores = self.sia.polarity_scores(text)
        compound_score = scores['compound']
        
        # Calculate anxiety level (0-10) based on negative sentiment
        # Compound score ranges from -1 to 1. 
        # If negative, we map it to anxiety. If positive, anxiety is low.
        anxiety_score = 0
        if compound_score < 0:
            anxiety_score = abs(compound_score) * 10
        elif scores['neg'] > 0.1:
            anxiety_score = scores['neg'] * 10
            
        is_panic = self._detect_panic(text, anxiety_score)
        pain_level = self._extract_pain_level(text)
        
        return {
            "sentiment_score": compound_score,
            "anxiety_level": round(anxiety_score, 2),
            "is_panic": is_panic,
            "pain_level": pain_level,
            "raw_scores": scores
        }

    def _detect_panic(self, text: str, anxiety_score: float) -> bool:
        """
        Detect urgency and panic in patient descriptions.
        """
        text_lower = text.lower()
        if any(keyword in text_lower for keyword in self.panic_keywords):
            return True
        if anxiety_score > 8.0:
            return True
        return False

    def _extract_pain_level(self, text: str) -> int:
        """
        Extract pain level (1-10) from text descriptions using regex.
        Returns 0 if no pain level is found.
        """
        # Patterns like "pain is 8/10", "pain level 5", "7 out of 10"
        patterns = [
            r"pain.*?(\d+)\s*/\s*10",
            r"pain.*?level.*?(\d+)",
            r"(\d+)\s*out of\s*10"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    level = int(match.group(1))
                    if 0 <= level <= 10:
                        return level
                except ValueError:
                    continue
                    
        return 0
