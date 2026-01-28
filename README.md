# 🩺 Medsy: AI-Powered Medical Companion

Medsy is a state-of-the-art, voice-activated medical assistant designed to bridge the gap between patients and healthcare providers. It provides intelligent symptom tracking, automated appointment booking, medical jargon translation, and critical emergency detection through a premium, responsive interface.

---

## 🌟 Overview

Medsy is built to handle the complexities of patient interaction with empathy and precision. Whether a patient is experiencing high anxiety, trying to understand a complex diagnosis, or simply needs to book a follow-up, Medsy provides a seamless, secure, and intelligent experience.

### Key Capabilities:

- **Intelligent Triage**: Detects life-threatening emergencies in real-time.
- **Empathetic Chat**: Analyzes patient sentiment to provide reassuring responses.
- **Medical Intelligence**: Simplifies complex jargon into "plain English."
- **Conversational Booking**: A robust state-machine driven appointment system.
- **Data Persistence**: Full medical history, medication logs, and appointment tracking.

---

## 🛠 Tech Stack & NLP Methods

### **Core Technology**

| Layer        | Technology                                   |
| :----------- | :------------------------------------------- |
| **Backend**  | Python 3.10+, FastAPI, Uvicorn               |
| **Frontend** | React 18, Vite, Tailwind CSS (Glassmorphism) |
| **Database** | SQLite, SQLAlchemy ORM                       |
| **DevOps**   | Docker, Multistage Build                     |

### **NLP & Artificial Intelligence**

Medsy employs a multi-layered NLP strategy to interpret medical context:

1.  **Sentiment Analysis (NLTK VADER)**:
    - **Method**: Lexicon-based sentiment scoring.
    - **Usage**: Detects anxiety levels (0-10) and identifies "Panic" states to trigger reassuring AI behaviors.
    - **Optimization**: LRU-cached for high performance.

2.  **Intent Classification (Scikit-Learn)**:
    - **Algorithm**: `RandomForestClassifier` with `TfidfVectorizer`.
    - **Scope**: Categorizes user queries into 6+ intents: `book_appointment`, `report_symptoms`, `emergency_alert`, `cancel_appointment`, etc.
    - **Data**: Trained on 600+ synthetic medical query examples.

3.  **Topic Modeling (LDA)**:
    - **Algorithm**: Latent Dirichlet Allocation (LDA).
    - **Usage**: Clusters symptoms from long patient descriptions into body systems (Respiratory, Neurological, etc.).

4.  **Emergency Detection**:
    - **Logic**: Rule-based scoring engine for critical symptoms (Heart Attack, Stroke, Anaphylaxis).
    - **Automation**: Triggers the `AlertSystem` for external notifications (SMS/Email simulation).

5.  **Voice Interaction**:
    - **STT**: `SpeechRecognition` (Google Web Speech API).
    - **TTS**: `pyttsx3` (Native OS voice engine).

---

## 📂 Folder Structure

```text
Medsy Medical Chatbot/
├── app/                        # Backend FastAPI Application
│   ├── core/                   # Configuration & Logging
│   ├── models/                 # SQLAlchemy DB Models & ML .pkl files
│   ├── routers/                # API Endpoints (Chat, Appointments, Voice)
│   ├── services/               # Core Logic (The "Brain")
│   │   ├── ai_generator.py      # LLM / OpenAI Integration
│   │   ├── appointment_flow.py  # Booking State Machine
│   │   ├── emergency_detector.py # Rule-based Triage
│   │   ├── sentiment_analyzer.py # VADER Sentiment Analysis
│   │   └── ...                  # Other modular services
│   └── main.py                 # App Entry Point
├── frontend/                   # React Vite Application
│   ├── src/
│   │   ├── components/         # Chat and Widget UI components
│   │   └── App.jsx             # Main Layout & Navigation
│   └── tailwind.config.js      # Custom Medical Theme
├── tests/                      # Pytest Suite (Unit & Integration)
├── Dockerfile                  # Containerization Config
├── requirements.txt            # Python Dependencies
└── README.md                   # This Documentation
```

---

## ⚙️ Implementation Details

### **1. The Appointment State Machine**

Unlike simple chatbots, Medsy uses a deterministic state machine for booking. This ensures that critical data (Problem, Date, Time) is collected reliably regardless of side conversations.

### **2. Premium Glassmorphism UI**

The frontend utilizes Tailwind's `backdrop-blur` and opacity scales to create a "clean-room" medical aesthetic. Animations are handled via Tailwind's `animate-in` utilities for smooth transitions.

### **3. Performance Optimization**

Critical NLP services are optimized with `@lru_cache`, reducing redundant processing for frequent medical terms and common patient greetings.

---

## 🚀 How to Execute

### **Step 1: Backend Setup**

1.  **Environment**: Navigate to the root directory.
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\\Scripts\\activate
    ```
2.  **Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run**:
    ```bash
    uvicorn app.main:app --reload
    ```
    _The API will be live at `http://localhost:8000`._

### **Step 2: Frontend Setup**

1.  **Navigate**:
    ```bash
    cd frontend
    ```
2.  **Install**:
    ```bash
    npm install
    ```
3.  **Run**:
    ```bash
    npm run dev
    ```
    _The UI will be live at `http://localhost:5173`._

### **Step 3: Execution & Testing**

- **To test the "Brain"**: Run `pytest tests/` from the root.
- **To view API Docs**: Visit `http://localhost:8000/docs`.
- **To run via Docker**:
  ```bash
  docker build -t medsy .
  docker run -p 8000:8000 medsy
  ```

---

## 📝 License

This project is developed for the Medsy Medical Assistant demonstration.

**Disclaimer**: This AI assistant is for demonstration purposes and should not be used for actual medical advice. Always consult a professional in emergencies.
