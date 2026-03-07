// camera-controller.js
// Modularized camera controller for ASL Translator - Cloud Compatible Version
// Uses browser MediaDevices API for camera access

class CameraController {
    constructor(config) {
        this.startButton = document.getElementById(config.startButtonId);
        this.stopButton = document.getElementById(config.stopButtonId);
        this.videoElement = document.getElementById(config.videoElementId);
        this.container = document.getElementById(config.containerId);
        this.canvas = document.getElementById(config.canvasId);
        this.overlayCanvas = document.getElementById(config.overlayCanvasId);
        this.onPrediction = config.onPrediction || null;
        this.predictionLog = [];
        this.isInitialized = false;
        this.stream = null;

        this.init();
    }

    init() {
        if (!this.startButton || !this.stopButton || !this.videoElement || !this.container) {
            console.warn('CameraController: Required elements not found.');
            return;
        }

        if (this.isInitialized) return;

        this.startButton.addEventListener('click', () => this.startCamera());
        this.stopButton.addEventListener('click', () => this.stopCamera());

        this.isInitialized = true;
        console.log('CameraController: Initialized with WebRTC');
    }

    async startCamera() {
        try {
            this.stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 640 },
                    height: { ideal: 480 },
                    facingMode: "user"
                }
            });

            this.videoElement.srcObject = this.stream;
            this.container.style.display = 'flex';
            this.container.classList.remove('hidden');

            this.stopButton.style.display = 'inline-block';
            this.stopButton.classList.remove('hidden');
            this.startButton.style.display = 'none';

            console.log('CameraController: Browser camera stream started');
        } catch (err) {
            console.error("CameraController: Error accessing camera:", err);
            alert("Could not access camera. Please ensure you have granted permissions.");
        }
    }

    stopCamera() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
        }

        if (this.videoElement) {
            this.videoElement.srcObject = null;
        }

        this.container.style.display = 'none';
        this.container.classList.add('hidden');

        this.stopButton.style.display = 'none';
        this.stopButton.classList.add('hidden');
        this.startButton.style.display = 'inline-block';

        console.log('CameraController: Camera stream stopped');
    }

    // Utility to capture frame for hybrid processing if needed
    captureFrame() {
        if (!this.canvas || !this.videoElement) return null;
        const context = this.canvas.getContext('2d');
        this.canvas.width = this.videoElement.videoWidth;
        this.canvas.height = this.videoElement.videoHeight;
        context.drawImage(this.videoElement, 0, 0, this.canvas.width, this.canvas.height);
        return this.canvas.toDataURL('image/jpeg');
    }

    capturePrediction(text) {
        if (!text) return;
        this.predictionLog.push({ text, timestamp: new Date().toISOString() });
        if (this.predictionLog.length > 10) this.predictionLog.shift();
        if (this.onPrediction) this.onPrediction(text);
    }
}

function initCameraController(config) {
    return new CameraController(config);
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { CameraController, initCameraController };
}
