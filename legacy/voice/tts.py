"""
Text-to-Speech using Google Gemini TTS models with gTTS fallback
"""
import os
import io
import base64
import tempfile
from typing import Optional
import google.generativeai as genai
from gtts import gTTS


class GeminiTTS:
    """Text-to-speech using Gemini's built-in TTS capability"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-2.5-flash-preview-tts"):
        """
        Initialize Gemini TTS
        
        Args:
            api_key: Google API key (reads from GENAI_API_KEY env var if not provided)
            model: Gemini TTS model to use
        """
        self.api_key = api_key or os.getenv("GENAI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("API key required. Set GENAI_API_KEY environment variable.")
        
        genai.configure(api_key=self.api_key)
        self.model_name = model
        self.model = genai.GenerativeModel(
            model,
            generation_config={
                "response_modalities": ["AUDIO"],  # Request audio output
            }
        )
        
        # Voice configuration for a sweet, feminine voice
        self.voice_config = {
            "speech_config": {
                "voice_config": {
                    "prebuilt_voice_config": {
                        "voice_name": "Aoede"  # Feminine voice option
                    }
                }
            }
        }
    
    import time

    def text_to_speech(self, text: str, voice_config: Optional[dict] = None) -> bytes:
        """
        Convert text to speech audio
        
        Args:
            text: Text to convert to speech
            voice_config: Optional voice configuration (tone, speed, etc.)
            
        Returns:
            Audio bytes (WAV or PCM format)
        """
        # Try Gemini TTS first
        start_tts = self.time.time()
        try:
            audio = self._gemini_tts(text, voice_config)
            end_tts = self.time.time()
            print(f"[TTS] Gemini TTS generation took {end_tts - start_tts:.2f} seconds.")
            return audio
        except Exception as e:
            # Check if it's a quota error
            error_str = str(e)
            if 'quota' in error_str.lower() or '429' in error_str:
                print(f"⚠ Gemini TTS quota exceeded, falling back to gTTS")
                start_gtts = self.time.time()
                audio = self._gtts_fallback(text)
                end_gtts = self.time.time()
                print(f"[TTS] gTTS fallback generation took {end_gtts - start_gtts:.2f} seconds.")
                return audio
            else:
                # Re-raise non-quota errors
                raise
    
    def _gemini_tts(self, text: str, voice_config: Optional[dict] = None) -> bytes:
        """Generate audio using Gemini TTS"""
        # Merge default voice config with any custom config
        config = voice_config or self.voice_config
        
        # Generate audio using Gemini TTS
        response = self.model.generate_content(
            text,
            generation_config=config
        )
        
        # Extract audio from response
        # Check various possible response formats
        if hasattr(response, 'audio'):
            return response.audio
        elif hasattr(response, 'parts'):
            for part in response.parts:
                if hasattr(part, 'inline_data'):
                    mime_type = getattr(part.inline_data, 'mime_type', '')
                    if 'audio' in mime_type:
                        # Audio might be base64 encoded or raw bytes
                        audio_data = part.inline_data.data
                        if isinstance(audio_data, bytes):
                            return audio_data
                        else:
                            # Try base64 decode with padding fix
                            try:
                                # Add padding if needed
                                missing_padding = len(audio_data) % 4
                                if missing_padding:
                                    audio_data += '=' * (4 - missing_padding)
                                return base64.b64decode(audio_data)
                            except:
                                # If decoding fails, data might already be bytes
                                return audio_data.encode() if isinstance(audio_data, str) else audio_data
        elif hasattr(response, 'candidates'):
            # Try candidates structure
            for candidate in response.candidates:
                if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                    for part in candidate.content.parts:
                        if hasattr(part, 'inline_data'):
                            mime_type = getattr(part.inline_data, 'mime_type', '')
                            if 'audio' in mime_type:
                                audio_data = part.inline_data.data
                                if isinstance(audio_data, bytes):
                                    return audio_data
                                else:
                                    try:
                                        missing_padding = len(audio_data) % 4
                                        if missing_padding:
                                            audio_data += '=' * (4 - missing_padding)
                                        return base64.b64decode(audio_data)
                                    except:
                                        return audio_data.encode() if isinstance(audio_data, str) else audio_data
        
        raise ValueError(f"No audio data in response. Response type: {type(response)}")
    
    def _gtts_fallback(self, text: str) -> bytes:
        """Fallback TTS using gTTS (free, unlimited)"""
        try:
            # Create gTTS object
            tts = gTTS(text=text, lang='en', slow=False)
            
            # Save to bytes buffer
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            
            return audio_buffer.read()
        except Exception as e:
            raise RuntimeError(f"gTTS generation failed: {e}")
    
    def speak(self, text: str, voice_config: Optional[dict] = None, play: bool = True):
        """
        Generate speech and optionally play it
        
        Args:
            text: Text to speak
            voice_config: Optional voice configuration
            play: Whether to play audio immediately (requires audio library)
            
        Returns:
            Audio bytes
        """
        audio_bytes = self.text_to_speech(text, voice_config)
        
        if play:
            self._play_audio(audio_bytes)
        
        return audio_bytes
    
    def _play_audio(self, audio_bytes: bytes):
        """Play audio bytes using available audio library"""
        try:
            start_convert = self.time.time()
            # Gemini TTS returns raw PCM audio (16-bit, 24kHz, mono)
            # Convert to WAV format first
            from pydub import AudioSegment
            import tempfile

            # Create AudioSegment from raw PCM
            # Gemini TTS typically outputs 24kHz, 16-bit, mono PCM
            audio = AudioSegment(
                data=audio_bytes,
                sample_width=2,  # 16-bit = 2 bytes
                frame_rate=24000,  # 24kHz
                channels=1  # mono
            )

            # Save as WAV and play with pygame
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
                audio.export(f.name, format='wav')
                temp_path = f.name
            end_convert = self.time.time()
            print(f"[TTS] PCM-to-WAV conversion and export took {end_convert - start_convert:.2f} seconds.")

            # Play with pygame
            import pygame
            start_play = self.time.time()
            pygame.mixer.init()
            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play()

            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            end_play = self.time.time()
            print(f"[TTS] Audio playback took {end_play - start_play:.2f} seconds.")

            # Cleanup
            pygame.mixer.music.unload()
            try:
                os.unlink(temp_path)
            except:
                pass

        except ImportError as e:
            print(f"⚠ Audio playback requires pydub and pygame: {e}")
            print("  Install with: pip install pydub pygame")
        except Exception as e:
            print(f"⚠ Audio playback error: {e}")
            # Save to file as fallback
            try:
                import tempfile
                with tempfile.NamedTemporaryFile(suffix='.pcm', delete=False, mode='wb') as f:
                    f.write(audio_bytes)
                    print(f"  Audio saved to {f.name} for manual playback")
            except:
                pass


# Example usage for testing
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    tts = GeminiTTS()
    print("Testing Gemini TTS...")
    audio = tts.speak("Hi Danny! I'm Nyra, your virtual girlfriend. It's so nice to finally talk to you!")
    print(f"Generated {len(audio)} bytes of audio")
