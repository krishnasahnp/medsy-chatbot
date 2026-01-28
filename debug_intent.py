from app.services.intent_classifier import IntentClassifier

ic = IntentClassifier()
result = ic.predict("I want to book an appointment")
print(f"Intent for 'I want to book an appointment': {result}")

result2 = ic.predict("Book appointment")
print(f"Intent for 'Book appointment': {result2}")
