# Voice System for GemniGF

This directory contains modular voice I/O components for the virtual girlfriend application.

## Modules

### `tts.py` - Text-to-Speech
- Uses Gemini's built-in TTS models (`gemini-2.5-flash-preview-tts`)
- Converts text responses to natural-sounding speech
- Supports multiple audio playback backends (pygame, pydub, OS default)

### `stt.py` - Speech-to-Text
- Uses Google's speech_recognition library
- Captures microphone input and converts to text
- Auto-calibrates for ambient noise
- Supports continuous listening mode

## Usage

```python
from voice.tts import GeminiTTS
from voice.stt import SpeechRecognizer

# Initialize
tts = GeminiTTS()
stt = SpeechRecognizer()

# Listen for speech
text = stt.listen(prompt="Speak now...")
print(f"You said: {text}")

# Speak response
tts.speak("Hi there! I heard you!")
```

## Dependencies

Install with:
```bash
pip install SpeechRecognition PyAudio pygame
```

Note: PyAudio on Windows may require installing from a wheel file.
Download from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

## Integration

The voice system is used by `app_voice.py` for the full voice-enabled chat experience.
