"""
Voice I/O module for GemniGF
Provides text-to-speech and speech-to-text capabilities
"""

from .tts import GeminiTTS
from .stt import SpeechRecognizer

__all__ = ['GeminiTTS', 'SpeechRecognizer']
