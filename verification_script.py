import sys
import os

# Add the project root to sys.path so we can import app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.services.sentiment_analyzer import SentimentAnalyzer
from app.services.intent_classifier import IntentClassifier
from app.services.topic_modeler import TopicModeler

def test_sentiment():
    print("\n--- Testing Sentiment Analysis ---")
    analyzer = SentimentAnalyzer()
    
    test_cases = [
        "I am feeling great today!",
        "My head hurts so much, pain is 8/10",
        "I am having a panic attack, please help me I can't breathe",
        "Just a regular checkup."
    ]
    
    for text in test_cases:
        result = analyzer.analyze(text)
        print(f"Text: {text}")
        print(f"Result: {result}")
        print("-" * 20)

def test_intent():
    print("\n--- Testing Intent Classification ---")
    classifier = IntentClassifier()
    # It will train on first run
    classifier.predict("warm up") 
    
    test_cases = [
        "I need to book an appointment with Dr. Smith",
        "I have a really bad headache and fever",
        "What are the side effects of aspirin?",
        "Help! I'm bleeding profusely!",
        "Cancel my appointment for tomorrow",
        "What are your opening hours?"
    ]
    
    for text in test_cases:
        result = classifier.predict(text)
        print(f"Text: {text}")
        print(f"Predicted Intent: {result}")
        print("-" * 20)

def test_topic():
    print("\n--- Testing Topic Modeling ---")
    modeler = TopicModeler()
    # It will train on first run
    
    test_cases = [
        "I have a runny nose and coughing a lot",
        "My stomach hurts and I feel nauseous",
        "I have a severe migraine and dizziness"
    ]
    
    for text in test_cases:
        result = modeler.get_topic(text)
        print(f"Text: {text}")
        print(f"Topic Result: {result}")
        print("-" * 20)

if __name__ == "__main__":
    try:
        test_sentiment()
        test_intent()
        test_topic()
        print("\nAll tests passed successfully!")
    except Exception as e:
        print(f"\nError during testing: {e}")
        import traceback
        traceback.print_exc()
