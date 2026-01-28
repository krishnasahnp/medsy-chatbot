from datetime import datetime
from fpdf import FPDF
import os

class PreAppointmentAssistant:
    def __init__(self):
        self.symptoms_log = []
        self.questions = [
            "When did this start?",
            "How often does it occur?",
            "On a scale of 1-10, how severe is it?",
            "What makes it better or worse?",
            "Any other symptoms with this?"
        ]
        
    def start_symptom_logging(self):
        """Returns the first question to ask."""
        self.symptoms_log = [] # Reset
        return self.questions[0]

    def process_answer(self, answer, question_idx):
        """
        Process user answer for question at index.
        Returns (next_question_str, is_finished_bool)
        """
        self.symptoms_log.append({
            "question": self.questions[question_idx],
            "answer": answer,
            "timestamp": datetime.now()
        })
        
        next_idx = question_idx + 1
        if next_idx < len(self.questions):
            return self.questions[next_idx], False
        else:
            return "Thank you. I have logged your symptoms.", True

    def generate_smart_questions(self, symptoms_summary):
        """
        Suggest relevant questions for the doctor based on symptoms.
        Simple keyword matching for now.
        """
        suggested = []
        text = symptoms_summary.lower()
        
        if "pain" in text:
            suggested.append("What kind of pain management is best for me?")
        if "fever" in text:
            suggested.append("Should I be worried about infection?")
        if "long" in text or "chronic" in text:
            suggested.append("Are there lifestyle changes that can help?")
            
        suggested.append("What tests might I need?")
        return suggested

    def generate_report(self, user_name, output_path="static/reports/symptom_report.pdf"):
        """Generate a PDF report of the logged symptoms."""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        pdf.cell(200, 10, txt=f"Pre-Appointment Symptom Report", ln=1, align='C')
        pdf.cell(200, 10, txt=f"Patient: {user_name}", ln=1, align='C')
        pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=1, align='C')
        pdf.ln(10)
        
        pdf.set_font("Arial", 'B', size=12)
        pdf.cell(200, 10, txt="Symptom Log:", ln=1)
        pdf.set_font("Arial", size=11)
        
        for entry in self.symptoms_log:
            pdf.multi_cell(0, 10, txt=f"Q: {entry['question']}\nA: {entry['answer']}")
            pdf.ln(2)
            
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        pdf.output(output_path)
        return output_path
