import unittest
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from app.services.nlp_processor import MedicalNLPProcessor

class TestMedicalNLP(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("Initializing NLP Engine for Testing...")
        cls.nlp = MedicalNLPProcessor()

    def test_regex_extraction(self):
        text = "Contact me at 555-0199 or test@example.com for an appointment on 25/12/2024"
        entities = self.nlp.extract_entities(text)
        self.assertEqual(entities['email'], "test@example.com")
        self.assertIn("555-0199", entities['phone']) # Basic check
        self.assertEqual(entities['date'], "25/12/2024")

    def test_intent_detection(self):
        self.assertEqual(self.nlp.detect_intent("I want to book an appointment"), "book_appointment")
        self.assertEqual(self.nlp.detect_intent("Please cancel my visit"), "cancel_appointment")
        self.assertEqual(self.nlp.detect_intent("I have a severe headache"), "symptom_check")

    def test_urgency_assessment(self):
        urgent_text = "I am having severe chest pain and difficulty breathing"
        normal_text = "I have a mild headache"
        
        self.assertTrue(self.nlp.assess_urgency(urgent_text)['is_urgent'])
        self.assertFalse(self.nlp.assess_urgency(normal_text)['is_urgent'])

    def test_preprocessing(self):
        text = "Pains and aching"
        result = self.nlp.preprocess_text(text)
        # Check if stemming/lemmatization happened (e.g., pains -> pain)
        # Note: PorterStemmer might stem 'aching' to 'ach'
        self.assertIn('pain', result['stemmed']) 

    def test_similarity(self):
        # "head hurting" should be similar to "headache"
        result = self.nlp.find_similar_symptom("head hurting")
        self.assertEqual(result['match'], "headache")
        
        # "tummy ache" should be similar to "stomach ache"
        result2 = self.nlp.find_similar_symptom("tummy ache")
        self.assertEqual(result2['match'], "stomach ache")

if __name__ == '__main__':
    unittest.main()
