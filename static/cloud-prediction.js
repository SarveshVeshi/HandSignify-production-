/**
 * cloud-prediction.js
 * Final Optimized Cloud-Compatible version for HandSignify.
 * Replicates the original OpenCV/MediaPipe Python aesthetic and stability.
 */

class CloudPredictor {
    constructor(config) {
        this.videoElement = document.getElementById(config.videoElementId);
        this.overlayCanvas = document.getElementById(config.overlayCanvasId);
        this.predictionEndpoint = 'https://handsignify-api.onrender.com/api/predict';

        // --- Tuning Parameters (Matching Original Stability) ---
        this.predictionInterval = 80; // High frequency for responsiveness
        this.smoothingFactor = 0.35; // Fine-tuned for steady yet responsive box
        this.visibilityTimeout = 500;

        // --- State Management ---
        this.lastPredictionTime = 0;
        this.isProcessing = false;
        this.lastPredictedChar = null;
        this.lastVisibleTime = 0;

        // --- Persistence Buffers ---
        this.rawLandmarks = null;
        this.smoothedBox = { x: 0, y: 0, w: 0, h: 0 };
        this.isBoxInitialized = false;

        if (this.overlayCanvas) {
            this.ctx = this.overlayCanvas.getContext('2d');
        }

        this.hands = new Hands({
            locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`
        });

        // MATCHING ORIGINAL PYTHON PARAMETERS
        this.hands.setOptions({
            maxNumHands: 1,
            modelComplexity: 1,
            minDetectionConfidence: 0.5,
            minTrackingConfidence: 0.5
        });

        this.hands.onResults((results) => this.handleResults(results));
        this.init();
    }

    init() {
        if (!this.videoElement) return;

        // Main Loop
        const processFrame = async () => {
            if (this.videoElement.readyState >= 2 && !this.isProcessing) {
                await this.hands.send({ image: this.videoElement });
            }
            requestAnimationFrame(processFrame);
        };
        requestAnimationFrame(processFrame);

        // Render Loop (60 FPS)
        const renderLoop = () => {
            this.drawOverlay();
            requestAnimationFrame(renderLoop);
        };
        requestAnimationFrame(renderLoop);
    }

    handleResults(results) {
        if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
            this.rawLandmarks = results.multiHandLandmarks[0];
            this.lastVisibleTime = Date.now();

            const now = Date.now();
            if (now - this.lastPredictionTime >= this.predictionInterval) {
                this.callPredictionAPI(this.rawLandmarks);
                this.lastPredictionTime = now;
            }
        } else if (Date.now() - this.lastVisibleTime > this.visibilityTimeout) {
            this.rawLandmarks = null;
            this.isBoxInitialized = false;
            const bubble = document.getElementById('predictionBubble');
            if (bubble && this.videoElement.id === 'cameraVideo') bubble.innerText = "—";
        }
    }

    async callPredictionAPI(landmarks) {
        try {
            const response = await fetch(this.predictionEndpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ landmarks: landmarks })
            });

            const data = await response.json();
            if (data.success && data.character) {
                const char = data.character;
                if (char !== this.lastPredictedChar) {
                    console.log(`[CloudPredictor] New prediction: ${char}`);
                    this.handleNewPrediction(char);
                    this.lastPredictedChar = char;
                }
            } else if (!data.success) {
                console.error(`[CloudPredictor] API Error: ${data.error}`);
            }
        } catch (err) {
            console.error(`[CloudPredictor] Fetch Error:`, err);
        }
    }

    drawOverlay() {
        if (!this.ctx || !this.overlayCanvas || !this.videoElement) return;

        this.overlayCanvas.width = this.videoElement.clientWidth;
        this.overlayCanvas.height = this.videoElement.clientHeight;
        const ctx = this.ctx;
        ctx.clearRect(0, 0, this.overlayCanvas.width, this.overlayCanvas.height);

        if (!this.rawLandmarks) return;

        // 1. Draw Skeleton (Matching original Rainbow Style)
        this.drawOriginalSkeleton(this.rawLandmarks);

        // 2. Draw Smoothed Bounding Box
        this.drawSmoothedStyle(this.rawLandmarks);
    }

    drawOriginalSkeleton(landmarks) {
        const ctx = this.ctx;
        const w = this.overlayCanvas.width;
        const h = this.overlayCanvas.height;

        // Draw connections with specific colors from original mp_drawing_styles
        HAND_CONNECTIONS.forEach(([start, end], index) => {
            ctx.beginPath();
            ctx.lineWidth = 4;

            // Color Mapping to replicate MediaPipe Python Default
            if (start >= 1 && end <= 4) ctx.strokeStyle = '#FFFFFF'; // Thumb
            else if (start >= 5 && end <= 8) ctx.strokeStyle = '#00FF00'; // Index
            else if (start >= 9 && end <= 12) ctx.strokeStyle = '#FFFF00'; // Middle
            else if (start >= 13 && end <= 16) ctx.strokeStyle = '#FF00FF'; // Ring
            else if (start >= 17 && end <= 20) ctx.strokeStyle = '#FF0000'; // Pinky
            else ctx.strokeStyle = '#00FF00'; // Wrist base

            ctx.moveTo(landmarks[start].x * w, landmarks[start].y * h);
            ctx.lineTo(landmarks[end].x * w, landmarks[end].y * h);
            ctx.stroke();
        });

        // Draw landmark points
        landmarks.forEach(lm => {
            ctx.beginPath();
            ctx.arc(lm.x * w, lm.y * h, 4, 0, 2 * Math.PI);
            ctx.fillStyle = '#FF0000'; // Red
            ctx.fill();
            ctx.strokeStyle = '#FFFFFF'; // White border
            ctx.lineWidth = 1.5;
            ctx.stroke();
        });
    }

    drawSmoothedStyle(landmarks) {
        const w = this.overlayCanvas.width;
        const h = this.overlayCanvas.height;

        let minX = 1, minY = 1, maxX = 0, maxY = 0;
        landmarks.forEach(lm => {
            if (lm.x < minX) minX = lm.x;
            if (lm.y < minY) minY = lm.y;
            if (lm.x > maxX) maxX = lm.x;
            if (lm.y > maxY) maxY = lm.y;
        });

        const padding = 25;
        const targetX = minX * w - padding;
        const targetY = minY * h - padding;
        const targetW = (maxX - minX) * w + padding * 2;
        const targetH = (maxY - minY) * h + padding * 2;

        // EMA Smoothing for the box
        if (!this.isBoxInitialized) {
            this.smoothedBox = { x: targetX, y: targetY, w: targetW, h: targetH };
            this.isBoxInitialized = true;
        } else {
            const alpha = this.smoothingFactor;
            this.smoothedBox.x = this.smoothedBox.x * (1 - alpha) + targetX * alpha;
            this.smoothedBox.y = this.smoothedBox.y * (1 - alpha) + targetY * alpha;
            this.smoothedBox.w = this.smoothedBox.w * (1 - alpha) + targetW * alpha;
            this.smoothedBox.h = this.smoothedBox.h * (1 - alpha) + targetH * alpha;
        }

        const box = this.smoothedBox;
        const ctx = this.ctx;

        // Draw the iconic Black Rectangle
        ctx.strokeStyle = '#000000';
        ctx.lineWidth = 5;
        ctx.strokeRect(box.x, box.y, box.w, box.h);

        // Draw Prediction Label (Matching FONT_HERSHEY_SIMPLEX bold)
        if (this.lastPredictedChar) {
            ctx.fillStyle = '#111111';
            ctx.font = 'bold 42px "Segoe UI", Roboto, Helvetica, Arial, sans-serif';
            ctx.textAlign = 'left';
            ctx.fillText(this.lastPredictedChar, box.x, box.y - 12);

            // Update UI 
            const b1 = document.getElementById('predictionBubble');
            if (b1 && this.videoElement.id === 'cameraVideo') b1.innerText = this.lastPredictedChar;
            const b2 = document.getElementById('predictionDisplayVoice');
            if (b2 && this.videoElement.id === 'cameraVideoVoice') b2.innerText = this.lastPredictedChar;
        }
    }

    handleNewPrediction(char) {
        window.dispatchEvent(new CustomEvent('new-prediction', { detail: { character: char } }));
    }
}

document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('cameraVideo')) {
        window.cloudPredictor1 = new CloudPredictor({
            videoElementId: 'cameraVideo',
            overlayCanvasId: 'overlayCanvas'
        });
    }
    if (document.getElementById('cameraVideoVoice')) {
        window.cloudPredictor4 = new CloudPredictor({
            videoElementId: 'cameraVideoVoice',
            overlayCanvasId: 'overlayCanvasVoice'
        });
    }
});

window.addEventListener('new-prediction', (e) => {
    const char = e.detail.character;
    console.log(`[EventListener] Received new-prediction: ${char}`);
    if (typeof accumulatedText !== 'undefined') {
        accumulatedText += char + " ";
        const o1 = document.getElementById('predictionOutput');
        if (o1) o1.innerText = accumulatedText;
        const o2 = document.getElementById('accumulatedTextVoice');
        if (o2) o2.innerText = accumulatedText;
        if (typeof isAutoSpeakEnabled !== 'undefined' && isAutoSpeakEnabled) speakText(char);
    } else {
        console.warn('[EventListener] accumulatedText is undefined. Initializing...');
        window.accumulatedText = char + " ";
    }
});
