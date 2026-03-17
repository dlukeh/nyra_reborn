# Voice-Enabled Virtual Girlfriend Setup

## Quick Start

### 1. Install PyAudio (Required for microphone input)

**Windows:**
PyAudio requires a binary wheel. Download and install:

```powershell
# Install from pip (may not work on all systems)
pip install PyAudio

# If that fails, download the wheel from:
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
# Then install: pip install PyAudio‑0.2.13‑cp313‑cp313‑win_amd64.whl
```

### 2. Run the Voice App

```powershell
python GemniGF\app_voice.py
```

## Features

### Voice Input (Speech-to-Text)
- ✓ Speak to Nyra using your microphone
- ✓ Auto-calibrates for ambient noise
- ✓ Uses Google Speech Recognition (free)
- ✓ 30-second listen timeout, 15-second phrase limit

### Voice Output (Text-to-Speech)
- 🚧 Gemini TTS integration ready (API may need updates)
- ✓ Modular design - easy to add other TTS engines
- ✓ Multiple playback backends (pygame, pydub, OS default)

### Dual Mode
- Switch between text and voice chat anytime
- Type "voice" in text mode to enable voice
- Say "text mode" in voice mode to switch back
- Say/type "exit" to quit

## Architecture

```
GemniGF/
├── app               # Original text-only chat
├── app_voice.py      # Voice-enabled chat (new!)
└── voice/
    ├── __init__.py   # Module exports
    ├── tts.py        # Text-to-Speech (Gemini TTS)
    ├── stt.py        # Speech-to-Text (Google SR)
    └── README.md     # Voice module docs
```

## Integration with Larger Project

The voice system is designed to be modular:

```python
# Use in your Flask API
from GemniGF.voice import SpeechRecognizer, GeminiTTS

@app.route('/api/listen', methods=['POST'])
def listen_endpoint():
    stt = SpeechRecognizer()
    text = stt.listen(timeout=10)
    return jsonify({'text': text})

@app.route('/api/speak', methods=['POST'])
def speak_endpoint():
    tts = GeminiTTS()
    text = request.json.get('text')
    audio = tts.text_to_speech(text)
    return Response(audio, mimetype='audio/wav')
```

## Troubleshooting

### PyAudio installation fails
- Download pre-built wheel from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
- Match your Python version (cp313 = Python 3.13)

### Microphone not working
- Check Windows microphone permissions
- Test with: `python GemniGF\voice\stt.py`

### TTS not working
- Gemini TTS API is in preview and may change
- Text responses will still work (voice input only mode)

## Notes

- Voice input is free (uses Google Speech Recognition)
- TTS may consume additional API quota when fully enabled
- For production, consider caching TTS audio or using alternative TTS engines
