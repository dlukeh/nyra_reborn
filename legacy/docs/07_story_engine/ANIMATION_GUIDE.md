# Nyra Animation Guide

## 🎬 How to Add Animated Videos

The animation system is now ready! Just add your video files and they'll work automatically.

## 📁 Video Files Needed

Place these MP4 files in: `GemniGF/static/media/`

### 1. **nyra_idle.mp4** (Idle/Listening Animation)
- Plays when Nyra is listening or waiting
- Should loop seamlessly
- Examples:
  - Subtle breathing
  - Occasional blinks
  - Small head movements
  - Relaxed expression

### 2. **nyra_speaking.mp4** (Speaking Animation)
- Plays when Nyra is talking
- Loops during TTS playback
- Examples:
  - Mouth movements (talking)
  - More expressive face
  - Head tilts
  - Hand gestures

## 🎨 Where to Get Videos

### Option 1: D-ID (Recommended - Easy!)
1. Go to https://www.d-id.com/
2. Upload your `Nyra.png`
3. Generate two videos:
   - **Idle**: Use calm, neutral script like "..." (minimal movement)
   - **Speaking**: Use any script for mouth movement
4. Download MP4s, rename them, drop in media folder

### Option 2: HeyGen
1. https://www.heygen.com/
2. Upload Nyra's image
3. Create avatar videos
4. Download and add to project

### Option 3: Runway ML
1. https://runwayml.com/
2. Use AI video generation
3. Create idle and speaking loops

### Option 4: Synthesia
1. https://www.synthesia.io/
2. Professional AI avatars
3. Generate videos from image

## 🚀 How It Works

**Current Setup:**
- ✅ Shows `Nyra.png` as idle (static image)
- ✅ Animation system ready
- ✅ Auto-detects when videos are added

**When you add videos:**
1. Drop `nyra_idle.mp4` in media folder
2. Drop `nyra_speaking.mp4` in media folder
3. Refresh browser (Ctrl + Shift + R)
4. **Done!** Videos will play automatically

**Behavior:**
- **Idle**: Loops `nyra_idle.mp4` (or shows image if no video)
- **Speaking**: Plays `nyra_speaking.mp4` when TTS starts
- **Auto-switches**: Returns to idle when done speaking
- **Smooth transitions**: 0.3s fade between states

## 📝 File Naming (Important!)

**Exact names required:**
```
nyra_idle.mp4       ← Idle animation
nyra_speaking.mp4   ← Speaking animation
```

**Case sensitive on some systems, so use lowercase!**

## 🎥 Video Specs (Recommended)

- **Format**: MP4 (H.264)
- **Resolution**: 1080x1080 or 1920x1080
- **Duration**: 
  - Idle: 5-10 seconds (seamless loop)
  - Speaking: 3-5 seconds (loops during TTS)
- **File size**: Keep under 5MB each for fast loading
- **Frame rate**: 30 FPS

## ✅ Testing

1. Add videos to `GemniGF/static/media/`
2. Open browser console (F12)
3. Look for messages:
   - `✓ Idle video loaded`
   - `✓ Speaking video loaded`
4. Send a message to Nyra
5. Watch her switch from idle → speaking → idle!

## 🎭 Current Status

**Right now:**
- ✅ Static image (Nyra.png) working
- ✅ Animation system active
- ⏳ Waiting for video files
- ✅ Will auto-upgrade when videos added

**No code changes needed** - just drop in the MP4 files!

## 💡 Pro Tips

1. **Test with short clips first** to verify they work
2. **Make seamless loops** - first and last frame should match
3. **Use video editing** to trim and loop perfectly
4. **Optimize file size** with Handbrake or similar tools
5. **Check browser console** for loading confirmation

---

Ready to animate Nyra! 🎬✨
