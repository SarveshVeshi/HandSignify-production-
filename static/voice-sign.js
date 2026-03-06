// voice-sign.js - Speech Recognition for ASL Translator
// Uses Web Speech API to convert voice to text, then displays ASL signs

(function () {
    'use strict';

    // Speech Recognition Setup
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition = null;
    let isListening = false;

    // DOM Elements
    let microphoneButton, startBtn, stopBtn, listeningIndicator,
        transcriptSection, transcriptDisplay, browserWarning,
        voiceErrorMessage, voiceSignOutput;

    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', function () {
        initializeElements();
        checkBrowserCompatibility();

        if (SpeechRecognition) {
            initVoiceRecognition();
        }
    });

    function initializeElements() {
        // Get all DOM elements
        microphoneButton = document.getElementById('microphoneButton');
        startBtn = document.getElementById('startListeningBtn');
        stopBtn = document.getElementById('stopListeningBtn');
        listeningIndicator = document.getElementById('listeningIndicator');
        transcriptSection = document.getElementById('transcriptSection');
        transcriptDisplay = document.getElementById('transcriptDisplay');
        browserWarning = document.getElementById('browserWarning');
        voiceErrorMessage = document.getElementById('voiceErrorMessage');
        voiceSignOutput = document.getElementById('voiceSignOutput');

        // New button elements
        const startSpeechBtn = document.getElementById('startSpeechBtn');
        const stopSpeechBtn = document.getElementById('stopSpeechBtn');
        const clearVoiceSignTextBtn = document.getElementById('clearVoiceSignTextBtn');
        const refinedTextBox = document.getElementById('refinedTextBox');

        // Add event listeners for new buttons
        if (startSpeechBtn) {
            startSpeechBtn.addEventListener('click', function () {
                synthesizeSpeech(refinedTextBox.value || transcriptDisplay.textContent);
            });
        }

        if (stopSpeechBtn) {
            stopSpeechBtn.addEventListener('click', function () {
                window.speechSynthesis.cancel();
                if (startSpeechBtn) startSpeechBtn.style.display = 'inline-flex';
                stopSpeechBtn.style.display = 'none';
            });
        }

        if (clearVoiceSignTextBtn) {
            clearVoiceSignTextBtn.addEventListener('click', function () {
                if (refinedTextBox) refinedTextBox.value = '';
                if (transcriptDisplay) transcriptDisplay.textContent = '';
                if (voiceSignOutput) {
                    voiceSignOutput.innerHTML = '';
                    voiceSignOutput.classList.add('hidden');
                }
            });
        }

        // Generate Signs from edited refined text
        const generateSignsBtn = document.getElementById('generateSignsFromEditBtn');
        if (generateSignsBtn) {
            generateSignsBtn.addEventListener('click', function () {
                generateSignsFromRefinedText();
            });
        }
    }


    function switchTab(targetTabId) {
        // Hide all tabs
        const allTabs = document.querySelectorAll('.tab-content');
        allTabs.forEach(tab => tab.classList.remove('active'));

        // Show target tab
        const targetTab = document.getElementById(targetTabId);
        if (targetTab) {
            targetTab.classList.add('active');
        }

        // Stop listening if switching away from voice tab
        if (targetTabId !== 'voiceSignTab' && isListening) {
            stopListening();
        }
    }

    function checkBrowserCompatibility() {
        if (!SpeechRecognition) {
            browserWarning.classList.remove('hidden');
            startBtn.disabled = true;
            startBtn.style.opacity = '0.5';
            startBtn.style.cursor = 'not-allowed';
        }
    }

    function initVoiceRecognition() {
        recognition = new SpeechRecognition();

        // Configuration
        recognition.lang = 'en-US';
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        // Event Handlers
        recognition.onstart = function () {
            isListening = true;
            microphoneButton.classList.add('mic-active');
            if (listeningIndicator) {
                listeningIndicator.classList.remove('hidden');
                listeningIndicator.style.display = 'block';
            }
            if (startBtn) startBtn.style.display = 'none';
            if (stopBtn) stopBtn.style.display = 'inline-block';
            if (voiceErrorMessage) voiceErrorMessage.style.display = 'none';
        };

        recognition.onresult = function (event) {
            const transcript = event.results[0][0].transcript;
            handleTranscript(transcript);
        };

        recognition.onerror = function (event) {
            handleError(event.error);
        };

        recognition.onend = function () {
            stopListening();
        };

        // Button event listeners
        startBtn.addEventListener('click', startListening);
        stopBtn.addEventListener('click', stopListening);
    }

    function startListening() {
        if (!recognition) {
            showError('Speech recognition is not available.');
            return;
        }

        try {
            // Clear previous results
            voiceSignOutput.innerHTML = '';
            voiceSignOutput.style.display = 'none';
            transcriptSection.style.display = 'none';
            voiceErrorMessage.style.display = 'none';

            recognition.start();
        } catch (error) {
            showError('Could not start speech recognition. Please try again.');
        }
    }

    function stopListening() {
        if (recognition && isListening) {
            recognition.stop();
        }

        // Reset UI
        isListening = false;
        microphoneButton.classList.remove('mic-active');
        if (listeningIndicator) listeningIndicator.style.display = 'none';
        if (startBtn) startBtn.style.display = 'inline-block';
        if (stopBtn) stopBtn.style.display = 'none';
    }

    function handleTranscript(transcript) {
        // Clean the transcript: uppercase and keep only A-Z, 0-9, and spaces
        const cleanedText = transcript.toUpperCase().replace(/[^A-Z0-9 ]/g, '');

        // Display raw transcript
        transcriptDisplay.textContent = cleanedText;
        transcriptSection.style.display = 'block';

        // Populate the refined text box with the transcript so the user can edit it
        const refinedTextBox = document.getElementById('refinedTextBox');
        if (refinedTextBox) {
            refinedTextBox.value = cleanedText;
        }

        // Check if there's any valid content
        if (!cleanedText.trim() || !/[A-Z0-9]/.test(cleanedText)) {
            showError('No valid text recognized. Please speak clearly and try again.');
            return;
        }

        // Convert text to sign images
        generateSignsFromRefinedText();
    }

    /**
     * Generates sign images using the current refined text box content.
     * This allows users to edit the text before generating signs.
     */
    function generateSignsFromRefinedText() {
        const refinedTextBox = document.getElementById('refinedTextBox');
        const textToConvert = refinedTextBox ? refinedTextBox.value.trim() : '';

        if (!textToConvert) {
            return;
        }

        convertTextToSign(textToConvert, 'voiceSignOutput', 'asl');

        // Show output container if there's content
        if (voiceSignOutput && voiceSignOutput.children.length > 0) {
            voiceSignOutput.style.display = 'flex';
            voiceSignOutput.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }

    function handleError(error) {
        let errorMessage = 'An error occurred with speech recognition.';

        switch (error) {
            case 'no-speech':
                errorMessage = 'No speech was detected. Please try again.';
                break;
            case 'audio-capture':
                errorMessage = 'No microphone was found. Please check your device.';
                break;
            case 'not-allowed':
                errorMessage = 'Microphone permission denied. Please allow microphone access.';
                break;
            case 'network':
                errorMessage = 'Network error occurred. Please check your connection.';
                break;
            case 'aborted':
                // User stopped - not an error
                return;
        }

        showError(errorMessage);
        stopListening();
    }

    function showError(message) {
        voiceErrorMessage.textContent = message;
        voiceErrorMessage.classList.remove('hidden');

        // Auto-hide after 5 seconds
        setTimeout(function () {
            voiceErrorMessage.classList.add('hidden');
        }, 5000);
    }

    function synthesizeSpeech(text) {
        // Cancel any ongoing speech
        window.speechSynthesis.cancel();

        if (!text || text.trim() === '') {
            showError('No text to speak. Please provide some text first.');
            return;
        }

        // Create utterance
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 1;
        utterance.pitch = 1;
        utterance.volume = 1;

        // Update buttons
        const startSpeechBtn = document.getElementById('startSpeechBtn');
        const stopSpeechBtn = document.getElementById('stopSpeechBtn');

        utterance.onstart = function () {
            if (startSpeechBtn) startSpeechBtn.style.display = 'none';
            if (stopSpeechBtn) stopSpeechBtn.style.display = 'inline-flex';
        };

        utterance.onend = function () {
            if (startSpeechBtn) startSpeechBtn.style.display = 'inline-flex';
            if (stopSpeechBtn) stopSpeechBtn.style.display = 'none';
        };

        utterance.onerror = function (event) {
            showError('Speech synthesis error: ' + event.error);
            if (startSpeechBtn) startSpeechBtn.style.display = 'inline-flex';
            if (stopSpeechBtn) stopSpeechBtn.style.display = 'none';
        };

        // Start speech synthesis
        window.speechSynthesis.speak(utterance);
    }

})();
