import speech_recognition as sr
import pyttsx3
import threading
import time

class VoiceHandler:
    def __init__(self, wake_word="medsy"):
        self.wake_word = wake_word.lower()
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.is_listening = False
        
        # Configure voice (optional)
        voices = self.engine.getProperty('voices')
        if voices:
            self.engine.setProperty('voice', voices[0].id) # Default to first voice

    def speak(self, text):
        """Convert text to speech."""
        print(f"Bot: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        """Listen for audio and return text."""
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio)
                print(f"User: {text}")
                return text.lower()
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                return None
            except sr.RequestError:
                print("API unavailable")
                return None

    def start_wake_word_detection(self, callback):
        """Continuous listening for wake word (Simulated for non-blocking)."""
        self.is_listening = True
        
        def _listen_loop():
            while self.is_listening:
                text = self.listen()
                if text and self.wake_word in text:
                    print(f"Wake word '{self.wake_word}' detected!")
                    callback()
                time.sleep(0.5)

        thread = threading.Thread(target=_listen_loop, daemon=True)
        thread.start()

    def stop_listening(self):
        self.is_listening = False

if __name__ == "__main__":
    # Test
    bot = VoiceHandler()
    bot.speak("Hello, I am Medsy.")
