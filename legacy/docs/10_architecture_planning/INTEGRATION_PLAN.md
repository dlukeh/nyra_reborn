# Nyra Integration Plan - Image/Video Display

## Recommended Architecture

### Option 1: Web App (Flask + WebSocket) ⭐ RECOMMENDED
**Best for:** Full-featured app with image/video, cross-platform

```
Frontend (Browser)              Backend (Flask)
┌─────────────────────┐        ┌──────────────────────┐
│ HTML/CSS/JS         │◄──────►│ Flask Server         │
│                     │        │                      │
│ ┌─────────────────┐ │        │ ┌──────────────────┐ │
│ │ Video/Image     │ │        │ │ Gemini Chat      │ │
│ │ (Nyra Avatar)   │ │        │ │ + Voice I/O      │ │
│ └─────────────────┘ │        │ └──────────────────┘ │
│                     │        │                      │
│ ┌─────────────────┐ │        │ ┌──────────────────┐ │
│ │ Voice Input     │ │◄──WS──►│ │ Audio Processing │ │
│ │ (Browser mic)   │ │        │ │ (STT/TTS)        │ │
│ └─────────────────┘ │        │ └──────────────────┘ │
│                     │        │                      │
│ ┌─────────────────┐ │        │                      │
│ │ Audio Player    │ │◄──────►│                      │
│ │ (Nyra voice)    │ │        │                      │
│ └─────────────────┘ │        └──────────────────────┘
└─────────────────────┘
```

**Pros:**
- ✅ Works on any device with a browser
- ✅ Easy to sync image/video with voice
- ✅ Can animate avatar (lip-sync, expressions)
- ✅ WebSocket = real-time, low latency
- ✅ Browser handles audio/video natively
- ✅ Can use existing Flask server code

**Files needed:**
```
GemniGF/
├── app_web.py              # Flask server with WebSocket
├── static/
│   ├── css/
│   │   └── style.css       # Nyra UI styling
│   ├── js/
│   │   └── nyra.js         # WebSocket, voice I/O
│   └── media/
│       ├── nyra.png        # Avatar image
│       └── nyra_idle.mp4   # Idle animation video
└── templates/
    └── nyra.html           # Main UI
```

---

### Option 2: Desktop GUI (Tkinter/PyQt)
**Best for:** Standalone desktop app

```python
# Video playback with opencv + Tkinter
import tkinter as tk
from PIL import Image, ImageTk
import cv2

# Display video loop
# Audio plays via pygame/pydub
# Voice input via SpeechRecognition
```

**Pros:**
- ✅ No browser needed
- ✅ Full OS integration
- ✅ Can use system tray

**Cons:**
- ❌ More complex video sync
- ❌ Platform-specific issues
- ❌ Harder to distribute

---

### Option 3: Electron App
**Best for:** Cross-platform desktop app with web tech

**Pros:**
- ✅ Web technologies (HTML/CSS/JS)
- ✅ Desktop app experience
- ✅ Easy packaging

**Cons:**
- ❌ Larger bundle size
- ❌ More setup complexity

---

## My Recommendation: Flask Web App

**Why:**
1. You already have Flask in the project (`server.py`)
2. Browser handles video/audio perfectly
3. Can access microphone via WebRTC
4. Easy to add animations (CSS, video, canvas)
5. Works on phone/tablet too
6. Can deploy remotely later

**Key Features to Add:**

### 1. **Animated Avatar**
- Idle animation MP4 (loops when not speaking)
- Speaking animation (plays during TTS)
- Emotion variants (happy, thinking, etc.)

### 2. **Voice Visualization**
- Waveform during your speech
- Lip-sync animation for Nyra
- Audio level indicators

### 3. **Real-time Communication**
- WebSocket for instant voice streaming
- Server-Sent Events for TTS chunks
- Low-latency audio playback

### 4. **Enhanced UX**
- Chat history sidebar
- Voice/text mode toggle
- Settings (voice speed, avatar choice)

---

## Implementation Phases

### Phase 1: Basic Web UI (1-2 hours)
- [ ] Flask route for main page
- [ ] Static image of Nyra
- [ ] Text chat interface
- [ ] Basic styling

### Phase 2: Voice Integration (2-3 hours)
- [ ] Browser microphone access (Web Speech API or WebSocket)
- [ ] Send audio to server → STT
- [ ] Receive TTS audio → play in browser
- [ ] Visual feedback (speaking indicator)

### Phase 3: Video/Animation (2-4 hours)
- [ ] MP4 idle loop
- [ ] Switch to "speaking" video on TTS
- [ ] Smooth transitions
- [ ] Optional: Lip-sync with audio analysis

### Phase 4: Polish (1-2 hours)
- [ ] Responsive design
- [ ] Error handling
- [ ] Loading states
- [ ] Voice settings

---

## Quick Start Code Snippets

### Flask Server with WebSocket
```python
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from GemniGF.voice import SpeechRecognizer, GeminiTTS

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('nyra.html')

@socketio.on('voice_input')
def handle_voice(audio_data):
    # Process audio → text → Gemini → TTS
    text = stt.recognize(audio_data)
    response = chat.send_message(text)
    audio = tts.text_to_speech(response.text)
    emit('voice_response', {
        'text': response.text,
        'audio': base64.b64encode(audio).decode()
    })
```

### Frontend (JavaScript)
```javascript
const socket = io();
const video = document.getElementById('nyra-video');

// Send voice to server
navigator.mediaDevices.getUserMedia({audio: true})
  .then(stream => {
    // Record and send chunks
  });

// Receive and play response
socket.on('voice_response', (data) => {
  // Show text
  displayText(data.text);
  
  // Play audio
  const audio = new Audio('data:audio/wav;base64,' + data.audio);
  audio.play();
  
  // Switch to speaking animation
  video.src = 'media/nyra_speaking.mp4';
  audio.onended = () => {
    video.src = 'media/nyra_idle.mp4';
  };
});
```

---

## Next Steps

Want me to build:
1. **Basic web UI** - Simple Flask page with Nyra's image + voice chat
2. **Desktop GUI** - Tkinter app with video playback
3. **Full web app** - Flask + WebSocket + animations

Let me know and I'll implement it! 🚀
