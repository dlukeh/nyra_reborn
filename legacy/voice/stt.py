"""
Speech-to-Text using speech_recognition library
"""
import speech_recognition as sr
from typing import Optional, Callable


class SpeechRecognizer:
    """Speech recognition for voice input"""
    
    def __init__(self, language: str = "en-US"):
        """
        Initialize speech recognizer
        
        Args:
            language: Language code for recognition (e.g., 'en-US', 'es-ES')
        """
        self.recognizer = sr.Recognizer()
        self.language = language
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise on first use
        with self.microphone as source:
            print("Calibrating microphone for ambient noise... Please wait.")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Microphone ready!")
    
    def listen(
        self,
        prompt: str = "Listening...",
        timeout: Optional[int] = None,
        phrase_time_limit: Optional[int] = None
    ) -> Optional[str]:
        """
        Listen for speech input and convert to text
        
        Args:
            prompt: Message to display while listening
            timeout: Seconds to wait for speech to start (None = wait indefinitely)
            phrase_time_limit: Max seconds for the phrase (None = no limit)
            
        Returns:
            Recognized text or None if recognition failed
        """
        print(prompt)
        
        try:
            with self.microphone as source:
                # Listen for audio
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
            
            # Recognize speech using Google Speech Recognition
            print("Processing speech...")
            text = self.recognizer.recognize_google(audio, language=self.language)
            return text
            
        except sr.WaitTimeoutError:
            print("No speech detected within timeout period.")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio. Please try again.")
            return None
        except sr.RequestError as e:
            print(f"Speech recognition service error: {e}")
            return None
        except Exception as e:
            print(f"Error during speech recognition: {e}")
            return None
    
    def listen_with_callback(
        self,
        callback: Callable[[str], None],
        stop_phrase: str = "exit",
        prompt: str = "Listening... (say 'exit' to stop)"
    ):
        """
        Continuously listen and call callback with recognized text
        
        Args:
            callback: Function to call with recognized text
            stop_phrase: Phrase to stop listening
            prompt: Message to display while listening
        """
        print(f"Starting continuous listening. Say '{stop_phrase}' to stop.")
        
        while True:
            text = self.listen(prompt=prompt)
            
            if text:
                print(f"You said: {text}")
                
                if stop_phrase.lower() in text.lower():
                    print("Stopping listening.")
                    break
                
                callback(text)
            else:
                # Give user feedback and try again
                print("Ready for next input...")


# Example usage for testing
if __name__ == "__main__":
    recognizer = SpeechRecognizer()
    
    print("\n=== Speech Recognition Test ===")
    print("Speak something when prompted...")
    
    text = recognizer.listen(prompt="Say something: ", timeout=10)
    
    if text:
        print(f"\nRecognized: {text}")
    else:
        print("\nNo speech recognized.")
