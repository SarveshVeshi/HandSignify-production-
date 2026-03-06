/**
 * realtime-interaction.js
 * Handles WebSocket connections and Speech Synthesis for HandSignify.
 * Adapted for the new premium UI with Socket.IO.
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
        const char = data.character;

        // Update Prediction Bubble (Tab 1)
        const bubble = document.getElementById('predictionBubble');
        if (bubble) bubble.innerText = char;

        // Update Live Display (Tab 4)
        const displayVoice = document.getElementById('predictionDisplayVoice');
        if (displayVoice) displayVoice.innerText = char;

        if (callbacks.onPrediction) {
            callbacks.onPrediction(char);
        }
    });

    // Stable prediction (for accumulation)
    socket.on('stable_prediction', (data) => {
        const char = data.character;
        console.log('✅ Stable prediction:', char);

        accumulatedText += char + " ";

        // Update Prediction Output (Tab 1 & Tab 4)
        const output = document.getElementById('predictionOutput');
        if (output) {
            output.innerText = accumulatedText;
        }

        const outputVoice = document.getElementById('accumulatedTextVoice');
        if (outputVoice) {
            outputVoice.innerText = accumulatedText;
        }

        if (callbacks.onStablePrediction) {
            callbacks.onStablePrediction(char, accumulatedText);
        }

        // Auto-speak logic
        if (isAutoSpeakEnabled && window.speechSynthesis) {
            speakText(char);
        }

        // Request refinement from backend if in Tab 3 (Voice/Refinement context)
        // or just generally if needed.
        if (socket && socket.connected) {
            socket.emit('refine_text', { 'text': accumulatedText });
        }
    });

    socket.on('refined_text_update', (data) => {
        // Only update Refined Text area if Voice → Sign tab is NOT active
        // (Tab 3 manages its own refined text from speech recognition)
        const voiceTab = document.getElementById('voiceToSignPanel');
        const isVoiceTabActive = voiceTab && voiceTab.classList.contains('active');
        const refinedBox = document.getElementById('refinedTextBox');
        if (refinedBox && !isVoiceTabActive) {
            refinedBox.value = data.refined_text;
        }

        if (callbacks.onRefinedText) {
            callbacks.onRefinedText(data.refined_text);
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

function clearAccumulatedText() {
    accumulatedText = "";
    const output = document.getElementById('predictionOutput');
    if (output) output.innerText = "";

    const bubble = document.getElementById('predictionBubble');
    if (bubble) bubble.innerText = "";

    const displayVoice = document.getElementById('predictionDisplayVoice');
    if (displayVoice) displayVoice.innerText = "—";

    const accumulatedVoice = document.getElementById('accumulatedTextVoice');
    if (accumulatedVoice) accumulatedVoice.innerText = "";
}

function getAccumulatedText() {
    return accumulatedText;
}

// Global initialization on load
document.addEventListener('DOMContentLoaded', () => {
    initWebSocket();
});
