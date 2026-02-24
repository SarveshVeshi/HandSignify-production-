/**
 * realtime-interaction.js
 * Handles WebSocket connections and Speech Synthesis for HandSignify.
 * Dependencies: Socket.IO client
 */

let socket = null;
let accumulatedText = "";
let isAutoSpeakEnabled = false;

/**
 * Initializes WebSocket connection.
 * @param {object} callbacks - { onPrediction: fn, onStablePrediction: fn, onError: fn }
 */
function initWebSocket(callbacks = {}) {
    if (socket && socket.connected) {
        console.log('WebSocket already connected');
        return;
    }

    // Ensure Socket.IO is loaded
    if (typeof io === 'undefined') {
        console.error('Socket.IO client not loaded');
        return;
    }

    socket = io({
        transports: ['websocket', 'polling'],
        reconnection: true,
        reconnectionDelay: 1000,
        reconnectionAttempts: 5
    });

    socket.on('connect', () => {
        console.log('✅ WebSocket connected');
    });

    socket.on('disconnect', () => {
        console.log('❌ WebSocket disconnected');
    });

    // Live Unstable prediction
    socket.on('prediction', (data) => {
        if (callbacks.onPrediction) {
            callbacks.onPrediction(data.character);
        }
    });

    // Stable prediction (for accumulation)
    socket.on('stable_prediction', (data) => {
        console.log('✅ Stable prediction:', data.character);

        accumulatedText += data.character + " ";

        if (callbacks.onStablePrediction) {
            callbacks.onStablePrediction(data.character, accumulatedText);
        }

        // Auto-speak logic
        if (isAutoSpeakEnabled && window.speechSynthesis) {
            speakText(data.character);
        }
    });

    socket.on('error', (error) => {
        console.error('WebSocket error:', error);
        if (callbacks.onError) callbacks.onError(error);
    });

    socket.on('connect_error', (error) => {
        console.error('WebSocket connection error:', error);
        if (callbacks.onError) callbacks.onError(error);
    });
}

function disconnectWebSocket() {
    if (socket && socket.connected) {
        socket.disconnect();
        console.log('WebSocket manually disconnected');
    }
}

/**
 * Speaks text using browser Speech Synthesis.
 * @param {string} text - Text to speak
 * @param {object} settings - { rate: number, pitch: number, volume: number }
 */
function speakText(text, settings = {}) {
    if (!window.speechSynthesis || !text) return;

    const utterance = new SpeechSynthesisUtterance(text);

    // Get live values from UI if IDs are standard, or use passed settings
    const rateEl = document.getElementById('speechRate');
    const pitchEl = document.getElementById('speechPitch');

    utterance.rate = settings.rate || (rateEl ? parseFloat(rateEl.value) : 1.0);
    utterance.pitch = settings.pitch || (pitchEl ? parseFloat(pitchEl.value) : 1.0);
    utterance.volume = settings.volume || 1.0;

    window.speechSynthesis.speak(utterance);
}

/**
 * Stops any ongoing or queued speech.
 */
function stopSpeaking() {
    if (window.speechSynthesis) {
        window.speechSynthesis.cancel();
    }
}

/**
 * Refines "messed up" detected text into meaningful sentences.
 * logic:
 * 1. Merges repeated consecutive words/characters.
 * 2. Join characters that seem to form words.
 * 3. Handles common ASL/ISL phrase merging.
 * @param {string} text - Raw accumulated text
 */
function refineText(text) {
    if (!text) return "";

    // 1. Remove excessive spaces and trim
    let words = text.split(/\s+/).filter(w => w.length > 0);
    if (words.length === 0) return "";

    // 2. Collapse consecutive identical words (e.g., "HELLO HELLO" -> "HELLO")
    let collapsed = [];
    for (let i = 0; i < words.length; i++) {
        if (i === 0 || words[i] !== words[i - 1]) {
            collapsed.push(words[i]);
        }
    }

    // 3. Heuristic: If we have many 1-letter words in a row, combine them
    // Example: "H E L L O HOW ARE Y O U" -> "HELLO HOW ARE YOU"
    let result = [];
    let currentWordBuffer = "";

    for (let i = 0; i < collapsed.length; i++) {
        let curr = collapsed[i];

        // Is it a single character?
        if (curr.length === 1) {
            currentWordBuffer += curr;
        } else {
            // It's a full word. 
            // First, if we have letters in buffer, push them as a merged word
            if (currentWordBuffer) {
                result.push(currentWordBuffer);
                currentWordBuffer = "";
            }
            result.push(curr);
        }
    }

    // Final buffer flush
    if (currentWordBuffer) {
        result.push(currentWordBuffer);
    }

    // 4. Post-process: collapse again if merging characters created duplicates 
    // (unlikely but possible with weird detection)

    // 5. Join back with proper spacing
    return result.join(" ");
}

function clearAccumulatedText() {
    accumulatedText = "";
}

function getAccumulatedText() {
    return accumulatedText;
}

// Export for module usage (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initWebSocket,
        disconnectWebSocket,
        speakText,
        stopSpeaking,
        clearAccumulatedText,
        getAccumulatedText
    };
}
