"""
Test Gemini TTS to verify voice output works
"""
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GemniGF.voice.tts import GeminiTTS

def test_tts():
    print("=" * 60)
    print("Testing Nyra's Voice (Gemini TTS)")
    print("=" * 60)
    
    load_dotenv()
    
    try:
        print("\n[1/3] Initializing Gemini TTS...")
        tts = GeminiTTS()
        print("✓ TTS initialized")
        
        print("\n[2/3] Generating speech...")
        test_text = "Hi Danny! I'm Nyra, your virtual girlfriend. It's so nice to finally talk to you with my voice!"
        
        audio_bytes = tts.text_to_speech(test_text)
        print(f"✓ Generated {len(audio_bytes)} bytes of audio")
        print(f"  First bytes: {audio_bytes[:20].hex()}")
        
        # Save to file for inspection
        with open("test_audio_output.bin", "wb") as f:
            f.write(audio_bytes)
        print(f"  Saved to test_audio_output.bin for inspection")
        
        print("\n[3/3] Playing audio...")
        tts._play_audio(audio_bytes)
        print("✓ Audio playback complete")
        
        print("\n" + "=" * 60)
        print("SUCCESS! Nyra's voice is working!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ TTS test failed: {e}")
        import traceback
        traceback.print_exc()
        
        print("\n" + "=" * 60)
        print("Note: Gemini TTS is in preview and API may change.")
        print("If this fails, voice input will still work (text responses).")
        print("=" * 60)

if __name__ == "__main__":
    test_tts()
