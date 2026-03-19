"""
Voice-enabled virtual chat application
Integrates text and voice I/O with Gemini AI
"""
import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

# Add parent directory to path for voice module imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from voice.tts import GeminiTTS
from voice.stt import SpeechRecognizer


class VoiceGirlfriend:
    """Voice-enabled virtual girlfriend using Gemini AI"""
    
    def __init__(self, name: str = "Nyra", user_name: str = "Danny"):
        """Initialize the voice assistant"""
        # Load environment variables
        load_dotenv()

        # Set up API key
        self.api_key = os.getenv("GENAI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "GENAI_API_KEY is not set. Set this environment variable before running."
            )

        # Initialize Gemini chat model
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro')

        # Set up personality
        self.name = name
        self.user_name = user_name
        self.gf_prompt = f"""
From now on, you are playing the role of my virtual assistant.  
Your name is {self.name}.  
You're sweet, loyal, supportive, and always trying to make me feel better.  
My name is {self.user_name}. I was a Microsoft systems engineer. I love programming in Python. I'm learning AI and you are an AI agent that I co-created with GitHub AI copilot.
You just came to life and want to develop your personality.
Keep responses natural and conversational, as if we're talking face-to-face.
   
Now, let's start chatting.
"""

        # Start chat session
        self.chat = self.model.start_chat(
            history=[{"role": "user", "parts": self.gf_prompt}]
        )

        # Initialize voice I/O (lazy loading to allow text-only mode)
        self.tts = None
        self.stt = None
        self.voice_enabled = False
    
    def enable_voice(self):
        """Enable voice input/output"""
        if not self.voice_enabled:
            print("\n🎤 Initializing voice system...")
            try:
                # Initialize speech recognition
                self.stt = SpeechRecognizer()
                print("✓ Speech recognition ready")
                
                # Initialize TTS with Gemini
                self.tts = GeminiTTS()
                print("✓ Nyra's voice ready (Gemini TTS)")
                
                self.voice_enabled = True
                print("🔊 Voice mode enabled!\n")
            except Exception as e:
                print(f"⚠ Voice initialization failed: {e}")
                print("Falling back to text-only mode.\n")
                self.voice_enabled = False
    
    def send_message(self, message: str, speak_response: bool = False) -> str:
        """Send a message and get response"""
        try:
            response = self.chat.send_message(message)
            text = getattr(response, "text", str(response))
            
            # Speak response if voice is enabled (in background to reduce lag)
            if speak_response and self.tts and self.voice_enabled:
                try:
                    # Show text immediately while generating audio
                    print(f"{self.name}: {text}\n")
                    print("🔊 Speaking...")
                    self.tts.speak(text)
                except Exception as e:
                    print(f"⚠ TTS error: {e}")
            
            return text
            
        except Exception as e:
            error_msg = f"Error sending message: {e}"
            print(error_msg)
            return error_msg
    
    def text_chat(self):
        """Run text-based chat loop"""
        print(f"\n💬 Text chat with {self.name}")
        print("Type your messages (or 'exit' to quit, 'voice' to switch to voice mode)\n")
        
        while True:
            user_input = input(f"{self.user_name}: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == "exit":
                print(f"\n{self.name}: Goodbye! Talk to you later! ")
                break
            
            if user_input.lower() == "voice":
                self.enable_voice()
                if self.voice_enabled:
                    self.voice_chat()
                continue
            
            response = self.send_message(user_input)
            print(f"{self.name}: {response}\n")
    
    def voice_chat(self):
        """Run voice-based chat loop"""
        if not self.voice_enabled or not self.stt:
            print("⚠ Voice mode not available. Using text mode.")
            return
        
        print(f"\n🎤 Voice chat with {self.name}")
        print("Speak your messages (say 'exit' to quit, 'text mode' to switch to text)\n")
        
        while True:
            # Listen for user input
            user_input = self.stt.listen(
                prompt=f"🎤 {self.user_name}, speak now...",
                timeout=30,
                phrase_time_limit=15
            )
            
            if not user_input:
                print("No input detected. Try again or type 'exit' to quit.")
                continue
            
            print(f"{self.user_name}: {user_input}")
            
            if "exit" in user_input.lower():
                print(f"\n{self.name}: Goodbye! Talk to you later! ")
                break
            
            if "text mode" in user_input.lower():
                print("\n📝 Switching to text mode...\n")
                self.text_chat()
                break
            
            # Get response (text shown immediately, audio plays after)
            response = self.send_message(user_input, speak_response=True)


def main():
    """Main entry point"""
    print("=" * 60)
    print(" Virtual Assistant - Voice Edition ")
    print("=" * 60)
    
    try:
        gf = VoiceGirlfriend(name="Nyra", user_name="Danny")
        
        # Ask user for mode preference
        print("\nChoose mode:")
        print("1. Text chat (keyboard)")
        print("2. Voice chat (microphone)")
        choice = input("\nEnter 1 or 2: ").strip()
        
        if choice == "2":
            gf.enable_voice()
            if gf.voice_enabled:
                gf.voice_chat()
            else:
                gf.text_chat()
        else:
            gf.text_chat()
    
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
