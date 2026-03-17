# Nyra Lip-Sync Integration Plan
# Adding Wav2Lip voice synchronization to existing Nyra setup

import os
import subprocess
import tempfile
from pathlib import Path

class NyraLipSync:
    """
    Integrates Wav2Lip with Nyra's existing TTS system
    """
    
    def __init__(self, base_image_path="static/media/Nyra.png"):
        self.base_image = base_image_path
        self.wav2lip_path = "wav2lip"  # Will need to install Wav2Lip
        self.temp_dir = tempfile.mkdtemp()
        
    def setup_wav2lip(self):
        """
        Setup Wav2Lip in the project directory
        """
        # Instructions for manual setup
        setup_instructions = """
        WAV2LIP SETUP INSTRUCTIONS:
        
        1. Clone Wav2Lip repository:
           git clone https://github.com/Rudrabha/Wav2Lip.git wav2lip
           
        2. Download the pre-trained model:
           cd wav2lip
           wget https://github.com/Rudrabha/Wav2Lip/releases/download/v1.0.0/wav2lip_gan.pth
           
        3. Install requirements:
           pip install -r requirements.txt
           
        4. Install additional dependencies:
           pip install opencv-python librosa
        """
        return setup_instructions
    
    def generate_lipsync_video(self, audio_file, output_path):
        """
        Generate lip-synced video from audio using Wav2Lip
        """
        if not os.path.exists(self.wav2lip_path):
            raise FileNotFoundError("Wav2Lip not installed. Run setup_wav2lip() first.")
            
        cmd = [
            "python", f"{self.wav2lip_path}/inference.py",
            "--checkpoint_path", f"{self.wav2lip_path}/wav2lip_gan.pth",
            "--face", self.base_image,
            "--audio", audio_file,
            "--outfile", output_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                return output_path
            else:
                raise Exception(f"Wav2Lip failed: {result.stderr}")
        except Exception as e:
            print(f"Error generating lip-sync: {e}")
            return None
    
    def process_tts_to_video(self, tts_audio_path, message_id):
        """
        Convert TTS audio to lip-synced video for web display
        """
        output_video = f"static/media/nyra_response_{message_id}.mp4"
        
        # Generate lip-sync video
        video_path = self.generate_lipsync_video(tts_audio_path, output_video)
        
        if video_path:
            return f"/static/media/nyra_response_{message_id}.mp4"
        else:
            # Fallback to static image if lip-sync fails
            return "/static/media/Nyra.png"

# Integration points for existing app_web.py:

def integrate_with_nyra_web():
    """
    Shows how to integrate with existing app_web.py
    """
    integration_code = '''
    # Add to app_web.py imports:
    from nyra_lipsync import NyraLipSync
    
    # Initialize lip-sync system:
    lipsync = NyraLipSync()
    
    # Modify the TTS response handling:
    @socketio.on('send_message')
    def handle_message(data):
        # ... existing chat logic ...
        
        # Generate TTS audio (existing code)
        audio_path = tts.generate_speech(response_text, f"temp_audio_{session_id}.wav")
        
        # NEW: Generate lip-sync video
        video_url = lipsync.process_tts_to_video(audio_path, session_id)
        
        # Send both audio and video to frontend
        emit('bot_response', {
            'text': response_text,
            'audio_url': f'/audio/{audio_filename}',
            'video_url': video_url,  # NEW: lip-sync video
            'timestamp': datetime.now().isoformat()
        })
    '''
    return integration_code

# Frontend integration for nyra.html:

def frontend_integration():
    """
    JavaScript changes needed for nyra.html
    """
    js_code = '''
    // Add to nyra.js:
    
    socket.on('bot_response', function(data) {
        // ... existing text handling ...
        
        // NEW: Handle lip-sync video
        if (data.video_url) {
            showNyraSpeaking(data.video_url);
        }
        
        // Play audio as before
        if (data.audio_url) {
            playAudio(data.audio_url);
        }
    });
    
    function showNyraSpeaking(videoUrl) {
        const idleVideo = document.getElementById('nyra-idle-video');
        const speakingVideo = document.getElementById('nyra-speaking-video');
        
        // Switch to speaking video with lip-sync
        speakingVideo.src = videoUrl;
        speakingVideo.style.display = 'block';
        idleVideo.style.display = 'none';
        
        // Return to idle when video ends
        speakingVideo.onended = function() {
            speakingVideo.style.display = 'none';
            idleVideo.style.display = 'block';
        };
    }
    '''
    return js_code

if __name__ == "__main__":
    # Example usage
    lipsync = NyraLipSync()
    print(lipsync.setup_wav2lip())