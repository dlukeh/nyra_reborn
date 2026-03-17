// Update Growth Tracker panel with new stats
function updateGrowthTracker(stats) {
    document.getElementById('growth-relationship').textContent = stats.relationship;
    document.getElementById('growth-technical').textContent = stats.technical + '%';
    document.getElementById('growth-sysadmin').textContent = stats.sysadmin + '%';
    document.getElementById('growth-personality').textContent = stats.personality;
}

// Ensure showSettingsModal is globally available
window.showSettingsModal = function() {
    document.getElementById('settings-modal').style.display = 'block';
    document.getElementById('modal-backdrop').style.display = 'block';
};
// Nyra - AI Girlfriend Web App JavaScript

// --- Socket.IO connection (optional, falls back to HTTP) ---
let socket;
try {
    if (typeof io !== 'undefined') {
        socket = io();
        console.log('🔌 Socket.IO initialized');
    } else {
        console.log('📡 Using HTTP mode (Socket.IO not available)');
    }
} catch (error) {
    console.log('📡 Fallback to HTTP mode:', error.message);
    socket = null;
}

// --- DOM Elements ---
const chatMessages = document.getElementById('chat-messages'); // Chat message container
const messageInput = document.getElementById('message-input'); // Text input field
const sendBtn = document.getElementById('send-btn'); // Send button
const toggleModeBtn = document.getElementById('toggle-mode'); // Toggle text/voice mode
const modeIcon = document.getElementById('mode-icon');
const modeText = document.getElementById('mode-text');
const textInputArea = document.getElementById('text-input-area');
const voiceInputArea = document.getElementById('voice-input-area');
const voiceBtn = document.getElementById('voice-btn');
const statusText = document.querySelector('.status-text');
const ttsAudio = document.getElementById('tts-audio');

// Avatar elements
const nyraIdleImage = document.getElementById('nyra-idle-image');
const nyraIdleVideo = document.getElementById('nyra-idle-video');
const nyraSpeakingImage = document.getElementById('nyra-speaking-image');
const nyraSpeakingVideo = document.getElementById('nyra-speaking-video');

// --- State ---
let isVoiceMode = false; // Whether voice mode is active
let sessionId = 'session_' + Date.now(); // Unique session ID
let isRecording = false; // Voice recording state
let mediaRecorder = null;
let audioChunks = [];
let hasIdleVideo = false;
let hasSpeakingVideo = false;

// --- Initialize app ---
init();

// Main initialization function
function init() {
    // Growth Tracker - update with backend data or placeholder
    updateGrowthTracker({
        relationship: 'Level 1',
        technical: 10,
        sysadmin: 5,
        personality: 'Sweet & Supportive'
    });
    // Set up event listeners and check media
    checkMediaAvailability();
    // Event listeners for chat and controls
    sendBtn.addEventListener('click', sendTextMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendTextMessage();
    });
    toggleModeBtn.addEventListener('click', toggleMode);
    voiceBtn.addEventListener('click', startWebSpeechRecognition);
    // Quick action buttons
    document.getElementById('clear-chat').addEventListener('click', clearChat);
    document.getElementById('save-log').addEventListener('click', saveChatLog);
    // Settings modal logic
    window.showSettingsModal = function() {
        document.getElementById('settings-modal').style.display = 'block';
        document.getElementById('modal-backdrop').style.display = 'block';
    };
    window.closeSettingsModal = function() {
        document.getElementById('settings-modal').style.display = 'none';
        document.getElementById('modal-backdrop').style.display = 'none';
    };

    // Dark mode toggle
    document.getElementById('dark-mode-toggle').addEventListener('change', function(e) {
        if (e.target.checked) {
            document.body.style.background = '#18181b';
            document.body.style.color = '#fafafa';
        } else {
            document.body.style.background = '';
            document.body.style.color = '';
        }
    });

    // Notifications toggle (placeholder)
    document.getElementById('notifications-toggle').addEventListener('change', function(e) {
        if (e.target.checked) {
            alert('Notifications enabled (feature coming soon)');
        }
    });
// Clear chat log
function clearChat() {
    chatMessages.innerHTML = '';
}

// Save chat log to file
function saveChatLog() {
    let log = '';
    document.querySelectorAll('.message').forEach(msg => {
        const sender = msg.classList.contains('user-message') ? 'You' : 'Nyra';
        const time = msg.querySelector('.message-time').textContent;
        const text = msg.querySelector('.message-content p').textContent;
        log += `[${time}] ${sender}: ${text}\n`;
    });
    const blob = new Blob([log], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'nyra_chat_log.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Show settings (placeholder)
function showSettings() {
    alert('Settings panel coming soon!');
}
    
    // Socket.IO events (if available)
    if (socket) {
        socket.on('connect', () => {
            updateStatus('Connected via WebSocket', 'success');
        });
        
        socket.on('disconnect', () => {
            updateStatus('WebSocket disconnected - using HTTP', 'warning');
        });
        
        socket.on('voice_response', handleVoiceResponse);
        socket.on('error', handleError);
    } else {
        // HTTP mode - show ready status
        updateStatus('Ready (HTTP Mode)', 'success');
    }
}

// Check which media files are available
function checkMediaAvailability() {
    // Check idle video
    nyraIdleVideo.addEventListener('loadeddata', () => {
        hasIdleVideo = true;
        console.log('✓ Idle video loaded');
    });
    
    nyraIdleVideo.addEventListener('error', () => {
        hasIdleVideo = false;
        console.log('ℹ No idle video - using image');
    });
    
    // Check speaking video
    nyraSpeakingVideo.addEventListener('loadeddata', () => {
        hasSpeakingVideo = true;
        console.log('✓ Speaking video loaded');
    });
    
    nyraSpeakingVideo.addEventListener('error', () => {
        hasSpeakingVideo = false;
        console.log('ℹ No speaking video - using image');
    });
    
    // Start in idle state
    setAvatarState('idle');
}

// Toggle between text and voice mode
function toggleMode() {
    isVoiceMode = !isVoiceMode;
    
    if (isVoiceMode) {
        textInputArea.style.display = 'none';
        voiceInputArea.style.display = 'flex';
        modeIcon.textContent = '🎤';
        modeText.textContent = 'Voice Mode';
    } else {
        textInputArea.style.display = 'flex';
        voiceInputArea.style.display = 'none';
        modeIcon.textContent = '⌨️';
        modeText.textContent = 'Text Mode';
    }
}

// Send text message
// Send message via HTTP API (used for both text and voice)
async function sendMessageViaHTTP(message) {
    if (!message) return;
    
    // Update status
    updateStatus('Thinking...', 'processing');
    
    try {
        // Send to server
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message, session_id: sessionId })
        });
        
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        // Add Nyra's response
        addMessage(data.response, 'bot');
        
        // BULLETPROOF: Check if memory was saved successfully
        if (data.bulletproof_memory) {
            console.log('🛡️ Memory saved successfully!');
        } else {
            console.warn('⚠️ Memory save may have failed!');
        }
        
        // Generate and play TTS
        await playTTS(data.response);
        
        updateStatus('Ready', 'success');
        
    } catch (error) {
        console.error('Error:', error);
        addMessage('Sorry, I had trouble responding. Please try again.', 'bot');
        updateStatus('Error', 'error');
    }
}

async function sendTextMessage() {
    const message = messageInput.value.trim();
    if (!message) return;
    
    // Add user message to chat
    addMessage(message, 'user');
    messageInput.value = '';
    
    // Use the shared HTTP function
    await sendMessageViaHTTP(message);
}

// Start voice recording
async function startVoiceRecording() {
    if (isRecording) return;
    
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];
        
        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };
        
        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            await processVoiceInput(audioBlob);
            
            // Stop all tracks
            stream.getTracks().forEach(track => track.stop());
        };
        
        mediaRecorder.start();
        isRecording = true;
        updateStatus('Listening...', 'recording');
        voiceBtn.classList.add('recording');
        
    } catch (error) {
        console.error('Microphone error:', error);
        alert('Could not access microphone. Please check permissions.');
    }
}

// Stop voice recording
function stopVoiceRecording() {
    if (!isRecording || !mediaRecorder) return;
    
    mediaRecorder.stop();
    isRecording = false;
    voiceBtn.classList.remove('recording');
    updateStatus('Processing...', 'processing');
}

// Process voice input (simplified - uses Web Speech API instead)
async function processVoiceInput(audioBlob) {
    // For now, we'll use browser's Web Speech API instead of sending audio
    // This is simpler and works offline
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    
    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        addMessage(transcript, 'user');
        
        // Send via socket or HTTP
        if (socket && socket.connected) {
            socket.emit('voice_chat', {
                message: transcript,
                session_id: sessionId
            });
        } else {
            // Fallback to HTTP API
            sendMessageViaHTTP(transcript);
        }
    };
    
    recognition.onerror = (error) => {
        console.error('Speech recognition error:', error);
        updateStatus('Error', 'error');
    };
    
    // Note: This won't actually use the audioBlob, browser handles it
    // If you want to send audio to server, implement audio upload here
}

// Use Web Speech API directly with enhanced error handling
function startWebSpeechRecognition() {
    console.log('🎙️ Starting Web Speech Recognition...');
    
    // Check for browser support
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        alert('Speech recognition not supported in this browser. Please use Chrome, Edge, or Safari.');
        return;
    }
    
    // Prevent multiple instances
    if (window.currentRecognition) {
        window.currentRecognition.abort();
        window.currentRecognition = null;
    }
    
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    window.currentRecognition = recognition;
    
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';
    recognition.maxAlternatives = 1;
    
    recognition.onstart = () => {
        console.log('🎤 Speech recognition started');
        updateStatus('Listening...', 'recording');
        document.getElementById('voice-status').textContent = '🎤 Listening... Speak now!';
        voiceBtn.style.backgroundColor = '#ff4444';
        voiceBtn.style.color = 'white';
    };
    
    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        console.log('📝 Transcript:', transcript);
        addMessage(transcript, 'user');
        
        // Send to server
        console.log('📤 Sending to server...');
        if (socket && socket.connected) {
            socket.emit('voice_chat', {
                message: transcript,
                session_id: sessionId
            });
        } else {
            // Fallback to HTTP API
            sendMessageViaHTTP(transcript);
        }
    };
    
    recognition.onerror = (error) => {
        console.error('❌ Speech error:', error.error, error);
        window.currentRecognition = null;  // Clear reference
        
        // CRITICAL: Don't lock up the interface - recover gracefully!
        updateStatus('Ready', 'success');  // Always reset to ready state
        document.getElementById('voice-status').textContent = '';
        voiceBtn.style.backgroundColor = '';
        voiceBtn.style.color = '';
        
        // Force memory save before handling error
        console.log('🛡️ Forcing memory save due to speech error...');
        
        let errorMessage = 'Speech issue (recovered): ';
        switch(error.error) {
            case 'not-allowed':
                errorMessage = '🎤 Microphone permission needed. Check browser settings and try again.';
                break;
            case 'no-speech':
                console.log('🔇 No speech detected - continuing normally');
                return; // Silent recovery
            case 'network':
                errorMessage = '🌐 Network hiccup - you can continue typing or try voice again.';
                break;
            case 'aborted':
                console.log('⏹️ Speech recognition stopped - continuing normally');
                return; // Silent recovery
            case 'audio-capture':
                errorMessage = '🎤 Microphone busy - try closing other apps or use text input.';
                break;
            default:
                errorMessage += error.error + ' - Interface recovered, you can continue.';
        }
        
        // Show brief non-blocking notification instead of alert
        console.warn(errorMessage);
        document.getElementById('voice-status').textContent = errorMessage;
        setTimeout(() => {
            document.getElementById('voice-status').textContent = '';
        }, 3000);
    };
    
    recognition.onend = () => {
        console.log('✓ Speech recognition ended');
        window.currentRecognition = null;  // Clear reference
        updateStatus('Ready', 'success');
        document.getElementById('voice-status').textContent = '';
        voiceBtn.style.backgroundColor = '';
        voiceBtn.style.color = '';
    };
    
    try {
        recognition.start();
        
        // Safety timeout - abort if no response in 10 seconds
        setTimeout(() => {
            if (window.currentRecognition === recognition) {
                recognition.abort();
                console.log('🕐 Speech recognition timed out');
            }
        }, 10000);
        
    } catch (error) {
        console.error('❌ Failed to start recognition:', error);
        window.currentRecognition = null;
        alert('Speech recognition failed: ' + error.message);
    }
}

// Voice button event handler is set in init() function

// Handle voice response from server
async function handleVoiceResponse(data) {
    // Add message to chat
    addMessage(data.text, 'bot');
    
    // Play audio if available
    if (data.audio) {
        await playTTSFromBase64(data.audio, data.format);
    }
    
    updateStatus('Ready', 'success');
}

// Play TTS audio
async function playTTS(text) {
    try {
        updateStatus('Speaking...', 'speaking');
        setAvatarState('speaking');
        
        const response = await fetch('/api/tts', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        await playTTSFromBase64(data.audio, data.format);
        
    } catch (error) {
        console.error('TTS error:', error);
        // Continue without audio
        setAvatarState('idle');
    }
}

// Play TTS from base64 encoded audio
async function playTTSFromBase64(audioB64, format) {
    return new Promise((resolve, reject) => {
        try {
            // Decode base64 to bytes
            const audioBytes = Uint8Array.from(atob(audioB64), c => c.charCodeAt(0));
            
            // Convert PCM to WAV format
            const wavBlob = pcmToWav(audioBytes, 24000, 1, 16);
            const audioUrl = URL.createObjectURL(wavBlob);
            
            ttsAudio.src = audioUrl;
            ttsAudio.onended = () => {
                setAvatarState('idle');
                updateStatus('Ready', 'success');
                URL.revokeObjectURL(audioUrl);
                resolve();
            };
            
            ttsAudio.onerror = () => {
                setAvatarState('idle');
                reject(new Error('Audio playback failed'));
            };
            
            ttsAudio.play();
            
        } catch (error) {
            setAvatarState('idle');
            reject(error);
        }
    });
}

// Convert PCM to WAV format
function pcmToWav(pcmData, sampleRate, numChannels, bitsPerSample) {
    const byteRate = sampleRate * numChannels * bitsPerSample / 8;
    const blockAlign = numChannels * bitsPerSample / 8;
    const dataSize = pcmData.length;
    
    const buffer = new ArrayBuffer(44 + dataSize);
    const view = new DataView(buffer);
    
    // RIFF header
    writeString(view, 0, 'RIFF');
    view.setUint32(4, 36 + dataSize, true);
    writeString(view, 8, 'WAVE');
    
    // fmt chunk
    writeString(view, 12, 'fmt ');
    view.setUint32(16, 16, true);  // chunk size
    view.setUint16(20, 1, true);   // PCM format
    view.setUint16(22, numChannels, true);
    view.setUint32(24, sampleRate, true);
    view.setUint32(28, byteRate, true);
    view.setUint16(32, blockAlign, true);
    view.setUint16(34, bitsPerSample, true);
    
    // data chunk
    writeString(view, 36, 'data');
    view.setUint32(40, dataSize, true);
    
    // Write PCM data
    for (let i = 0; i < pcmData.length; i++) {
        view.setUint8(44 + i, pcmData[i]);
    }
    
    return new Blob([buffer], { type: 'audio/wav' });
}

function writeString(view, offset, string) {
    for (let i = 0; i < string.length; i++) {
        view.setUint8(offset + i, string.charCodeAt(i));
    }
}

// Add message to chat
function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const now = new Date();
    const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    messageDiv.innerHTML = `
        <div class="message-content">
            <p>${escapeHtml(text)}</p>
        </div>
        <div class="message-time">${timeStr}</div>
    `;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Update status indicator
function updateStatus(text, state) {
    statusText.textContent = text;
    const statusDot = document.querySelector('.status-dot');
    
    statusDot.style.background = {
        'success': '#10b981',
        'error': '#ef4444',
        'processing': '#f59e0b',
        'recording': '#ff4d8f',
        'speaking': '#a855f7'
    }[state] || '#10b981';
}

// Set avatar state (idle/speaking)
function setAvatarState(state) {
    const avatarContainer = document.querySelector('.avatar-container');
    
    // Remove all active classes
    document.querySelectorAll('.avatar-media').forEach(el => {
        el.classList.remove('active');
    });
    
    if (state === 'speaking') {
        avatarContainer.classList.add('speaking');
        
        // Use speaking video if available, otherwise use image
        if (hasSpeakingVideo) {
            nyraSpeakingVideo.classList.add('active');
            nyraSpeakingVideo.play();
        } else {
            nyraSpeakingImage.classList.add('active');
        }
        
    } else {
        // Idle state
        avatarContainer.classList.remove('speaking');
        
        // Use idle video if available, otherwise use image
        if (hasIdleVideo) {
            nyraIdleVideo.classList.add('active');
            nyraIdleVideo.play();
        } else {
            nyraIdleImage.classList.add('active');
        }
        
        // Stop speaking video if it was playing
        if (hasSpeakingVideo) {
            nyraSpeakingVideo.pause();
            nyraSpeakingVideo.currentTime = 0;
        }
    }
}

// Handle errors
function handleError(data) {
    console.error('Error:', data);
    addMessage('Sorry, something went wrong. Please try again.', 'bot');
    updateStatus('Error', 'error');
}

// Escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
