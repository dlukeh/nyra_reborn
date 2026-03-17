# Nyra - Virtual Girlfriend AI Project Summary

## 🎯 What We Built

A complete voice-enabled AI girlfriend web application with animated avatar using Google's Gemini AI.

---

## 📁 Project Structure

```
GemniGF/
├── app                          # Original text chat (secured)
├── app_voice.py                 # Terminal-based voice chat
├── app_web.py                   # Flask web server ⭐ MAIN APP
├── .env                         # API key (secured, git-ignored)
├── requirements.txt             # All dependencies
│
├── voice/                       # Voice modules
│   ├── __init__.py
│   ├── tts.py                   # Gemini TTS (text-to-speech)
│   └── stt.py                   # Google Speech Recognition
│
├── templates/
│   └── nyra.html                # Web UI with avatar & chat
│
├── static/
│   ├── css/
│   │   └── style.css            # Gradient theme + animations
│   ├── js/
│   │   └── nyra.js              # Chat logic + animation control
│   └── media/
│       ├── Nyra.png             # Static avatar image
│       ├── nyra_speaking.mp4    # Lip sync animation ⭐
│       └── (nyra_idle.mp4)      # [TODO: Add idle animation]
│
├── ANIMATION_GUIDE.md           # Video creation guide
└── PROJECT_SUMMARY.md           # This file
```

---

## 🚀 How to Run

### Start the Server
```powershell
cd "c:\Users\danie\Labs\1st AI agent\GemniGF"
python app_web.py
```

### Access the App
Open browser to: **http://localhost:5001**

### Stop the Server
Press `Ctrl+C` in terminal

---

## 🎨 Features Implemented

### ✅ Core Features
- **Gemini AI Chat**: Powered by `gemini-2.0-flash` model
- **Voice Input**: Speech recognition via microphone
- **Voice Output**: Gemini TTS with natural-sounding speech
- **Text Chat**: Traditional text input option
- **Real-time Communication**: WebSocket (Socket.IO) for instant responses
- **Session Management**: Per-user chat history

### ✅ Avatar Animation System
- **State-based animations**: Idle ↔ Speaking
- **Video support**: MP4 playback with seamless looping
- **Fallback system**: Uses static image if videos unavailable
- **Auto-detection**: Checks for videos on page load
- **Smooth transitions**: 0.3s fade between states

### ✅ User Interface
- **Beautiful gradient design**: Pink/purple theme
- **Responsive layout**: Works on desktop & mobile
- **Mode toggle**: Switch between text/voice input
- **Status indicators**: Real-time feedback (Listening, Thinking, Speaking)
- **Chat history**: Scrollable message display

---

## 🔑 Configuration

### Environment Variables (.env)
```bash
GENAI_API_KEY=AIzaSyC5yMDhpzAkx5L3Xd3Jop2dNj6tswNvpBw
```

### Server Settings (in app_web.py)
```python
HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 5001       # Default port
DEBUG = True      # Enable debug mode
```

---

## 📦 Dependencies

### Core Libraries
```
google-generativeai>=0.4.0    # Gemini AI SDK
Flask>=2.0.0                  # Web framework
flask-socketio>=5.5.0         # Real-time WebSocket
python-dotenv>=0.21.0         # Environment variables
```

### Voice Processing
```
SpeechRecognition>=3.10.0     # Speech-to-text
PyAudio>=0.2.14               # Microphone input
pygame>=2.5.0                 # Audio playback
pydub>=0.25.0                 # Audio format conversion
```

### Install All
```powershell
pip install -r requirements.txt
```

---

## 🎬 Animation System

### Current Status
- ✅ `nyra_speaking.mp4` - Lip sync animation (working!)
- ⏳ `nyra_idle.mp4` - Idle animation (add later)

### How It Works
1. **Page loads**: JavaScript checks for video files
2. **User sends message**: Avatar switches to "idle" state
3. **Nyra responds**: Avatar switches to "speaking" state + plays TTS audio
4. **Response complete**: Returns to "idle" state

### Adding/Updating Videos
1. Place MP4 files in: `static/media/`
2. Use exact names: `nyra_idle.mp4`, `nyra_speaking.mp4`
3. Refresh browser (Ctrl + Shift + R)
4. Done! Auto-detected and used

### Recommended Specs
- **Format**: MP4 (H.264)
- **Resolution**: 1080x1080 or 1920x1080
- **Duration**: 3-10 seconds (seamless loop)
- **File size**: Under 5MB each
- **Frame rate**: 30 FPS

---

## 🛠️ Technical Details

### Gemini Models Used
- **Chat**: `gemini-2.0-flash` (text generation)
- **TTS**: `gemini-2.5-flash-preview-tts` (voice synthesis)

### Audio Processing Pipeline
1. **TTS Generation**: Gemini returns base64-encoded PCM audio
2. **Decoding**: Base64 → raw PCM bytes
3. **Conversion**: PCM → WAV (24kHz, 16-bit, mono)
4. **Playback**: pygame plays WAV file
5. **Frontend**: Web Audio API plays from base64

### API Endpoints

#### REST API
- `GET /` - Main web interface
- `POST /api/chat` - Text chat (JSON: `{message: string}`)
- `POST /api/tts` - Generate TTS audio (JSON: `{text: string}`)

#### WebSocket Events
- `voice_chat` - Real-time voice interaction
  - Emit: `{audio: base64, format: "wav"}`
  - Receive: `{response: string, audio: base64}`

---

## 🔒 Security Features

### ✅ Implemented
- API key in `.env` file (not in code)
- `.gitignore` excludes sensitive files
- Environment variable validation
- Graceful error handling for missing keys

### 🔐 Best Practices
- **Never commit** `.env` to git
- **Rotate API key** if exposed
- **Use HTTPS** in production
- **Add authentication** before public deployment

---

## 🎯 Development Timeline

### Phase 1: Security ✅
- Removed hard-coded API key
- Implemented environment variables
- Fixed import typos
- Added `.gitignore`

### Phase 2: Voice Integration ✅
- Implemented Gemini TTS
- Added speech recognition
- Built PCM to WAV converter
- Created voice modules (`tts.py`, `stt.py`)

### Phase 3: Terminal App ✅
- Built `app_voice.py`
- Tested voice input/output
- Validated audio pipeline

### Phase 4: Web Application ✅
- Created Flask server (`app_web.py`)
- Designed beautiful UI (`nyra.html`)
- Implemented WebSocket communication
- Added dual-mode chat (text/voice)

### Phase 5: Avatar System ✅
- Integrated static image (`Nyra.png`)
- Built animation framework
- Implemented state management
- Added video detection & fallback
- **TESTED**: Lip sync working! 🎉

---

## 📝 Next Steps (Future Development)

### Immediate
1. ✅ ~~Create speaking animation~~ (DONE!)
2. ⏳ Create idle animation (`nyra_idle.mp4`)
3. ⏳ Fine-tune lip sync quality

### Short-term
- Add emotion detection (happy, sad, etc.)
- Multiple animation states
- Background music/ambience
- User preferences (voice, personality)
- Chat export/history

### Long-term Integration
- Integrate into larger application
- Multi-user support
- Database for persistent history
- Advanced personality customization
- Memory system (remembers conversations)

---

## 🐛 Known Issues & Solutions

### Issue: Video not loading
**Solution**: Check filename is exactly `nyra_idle.mp4` or `nyra_speaking.mp4` (lowercase!)

### Issue: Audio not playing
**Solution**: Check browser console (F12) for errors. Ensure microphone permissions granted.

### Issue: WebSocket disconnects
**Solution**: Restart Flask server (`Ctrl+C`, then `python app_web.py`)

### Issue: API key errors
**Solution**: Verify `.env` file exists with `GENAI_API_KEY=your_key_here`

---

## 💡 Tips & Tricks

### Browser Cache
- **Hard refresh**: `Ctrl + Shift + R` (clears cache)
- Use when updating videos/images

### Console Debugging
- Press `F12` to open browser console
- Look for messages:
  - `✓ Idle video loaded`
  - `✓ Speaking video loaded`
  - `ℹ No idle video - using image`

### Video Creation
- **D-ID**: https://studio.d-id.com/ (easiest!)
- **HeyGen**: https://www.heygen.com/
- **Runway ML**: https://runwayml.com/

### Testing Videos
1. Add to `static/media/`
2. Hard refresh browser
3. Check console for confirmation
4. Send message to test

---

## 📚 File Reference

### Main Application Files

**app_web.py** - Flask web server
- Routes: `/`, `/api/chat`, `/api/tts`
- WebSocket: `voice_chat` event
- Session management
- TTS initialization

**nyra.html** - Web interface
- Avatar display (4 layers: idle/speaking × image/video)
- Chat interface
- Mode toggle (text/voice)
- Socket.IO client

**nyra.js** - Frontend logic
- `checkMediaAvailability()` - Detects videos
- `setAvatarState(state)` - Switches idle/speaking
- `sendMessage()` - Text chat handler
- `startVoiceChat()` - Voice input handler
- `playTTSFromBase64()` - Audio playback

**style.css** - Styling
- Gradient theme (pink/purple)
- Animation transitions
- Responsive layout
- Avatar state classes

**voice/tts.py** - Text-to-speech
- `GeminiTTS` class
- PCM to WAV conversion
- Audio playback

**voice/stt.py** - Speech recognition
- `SpeechRecognizer` class
- Microphone input
- Google Speech API

---

## 🎓 Key Learnings

1. **Gemini TTS requires**: `response_modalities: ["AUDIO"]` in config
2. **Audio format**: Raw PCM needs WAV header for playback
3. **WebSocket**: Perfect for real-time voice/chat
4. **Animation system**: Layer-based approach with opacity transitions
5. **Security**: Never hard-code API keys!

---

## 🤝 Credits

**Built with:**
- Google Gemini AI (chat & TTS)
- Flask & Socket.IO (web framework)
- D-ID (animation generation)
- Your creativity! 🎨

**Developed:** October 2025

---

## 📞 Quick Commands Reference

### Start Server
```powershell
cd "c:\Users\danie\Labs\1st AI agent\GemniGF"
python app_web.py
```

### Install Dependencies
```powershell
pip install -r requirements.txt
```

### Test Voice (Terminal)
```powershell
python app_voice.py
```

### Check Files
```powershell
dir static\media
```

### Rename Video
```powershell
Move-Item "static\media\video.mp4" "static\media\nyra_speaking.mp4"
```

---

## 🎉 Current Status: WORKING! ✅

- ✅ Server running on port 5001
- ✅ Voice chat functional
- ✅ Text chat functional
- ✅ TTS audio playing
- ✅ Avatar displaying
- ✅ **Animation system working!** 🎬
- ⏳ Ready for idle video addition

**Next up:** Fine-tune animations and prepare for larger app integration!

---

*Keep building amazing things! 🚀*
