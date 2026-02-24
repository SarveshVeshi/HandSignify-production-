# HandSignify Project Documentation & Technical Report

This document provides a comprehensive overview of the HandSignify project, including its architecture, logic, and a detailed analysis of the technical challenges encountered during development.

---

## 🏗️ Project Architecture

HandSignify is built using a **Flask** backend combined with a modern **Vanilla CSS/JS** frontend. It utilizes **MediaPipe** for hand landmark detection and a **Random Forest** model for sign language classification.

### 🧩 System Components
1.  **Backend (Flask)**: Handles routing, session management, and the core machine learning inference loop.
2.  **Streaming Interface (MJPEG)**: Provides a low-latency video feed using `multipart/x-mixed-replace`.
3.  **Real-Time Data (Socket.IO)**: Bridges the gap between the server's detection loop and the frontend's UI, sending predictions as WebSocket events.
4.  **Speech Synthesis**: Utilizes the browser's native **Web Speech API** (`speechSynthesis`) to convert recognized text into audible speech.

---

## 🛠️ Core Dependencies & Environment

To ensure stability, the project must run in a specific environment.

| Dependency | Version (Approx.) | Purpose |
| :--- | :--- | :--- |
| **Python** | **3.10.x** | **CRITICAL**: Higher versions (like 3.13) fail with MediaPipe compatibility. |
| **Flask** | 2.x - 3.x | Web framework and routing. |
| **Flask-SocketIO** | 5.3.6 | WebSocket support for real-time predictions. |
| **MediaPipe** | 0.10.x | Hand landmark detection and processing. |
| **OpenCV** | 4.x | Camera capture and image processing. |
| **Scikit-learn** | 1.x | Random Forest model inference. |
| **Eventlet** | 0.33.x | Concurrent worker for handling WebSockets and MJPEG simultaneously. |

---

## 🧠 Backend & Frontend Logic

### Frontend Logic
- **Tabbed Navigation**: The project is split into three distinct tabs to ensure separation of concerns:
    - **Tab 1**: Simple Sign-to-Text conversion.
    - **Tab 2**: Form-based Text-to-Sign conversion (GIF-based).
    - **Tab 3**: Advanced Sign-to-Text with automated Speech-on-Stop.
- **JavaScript Controllers**:
    - `camera-controller.js`: Manages the `<img>` tag source and buttons.
    - `realtime-interaction.js`: Manages the WebSocket connection and text accumulation.
    - `sign-voice.js`: Handles the speech synthesis engine.

### Backend Logic
- **`generate_frames()`**: A generator function that captures frames from the webcam, processes them through MediaPipe, makes a prediction using the Pickle model, and yields the frame as a byte stream.
- **WebSocket Emission**: Inside the frame loop, `socketio.emit` sends the results to the frontend.
- **Non-Blocking Yields**: `socketio.sleep(0)` is used to ensure the camera loop doesn't "starve" the WebSocket connection.

---

## ⚠️ Problems Faced & Solutions

### 1. The HTML `<img>` Tag vs. Video Tags (MJPEG)
- **Problem**: In the original repo, the camera was handled via complex JavaScript that often failed when the backendMJPEG stream was used.
- **Solution**: We reverted to the reliable `<img src="/video_feed">` method. However, we had to ensure JavaScript didn't "break" the stream by attempting to treat it as a static image. We implemented a clean `CameraController` to handle starting/stopping the stream without page refreshes.

### 2. WebSocket Connection Errors (Socket.IO)
- **Problem**: The original code imported `SocketIO` from the wrong library (`from socket import SocketIO`) and started the server with `app.run()`. This caused the frontend to stay permanently disconnected from predictions.
- **Solution**: We corrected the imports to `from flask_socketio import SocketIO` and switched the entry point to `socketio.run()`. This established the stable bridge required for real-time text updates.

### 3. MJPEG Blocking the Event Loop
- **Problem**: MJPEG streaming is a "blocking" operation because it keeps a connection open forever. This often caused the WebSocket connection to timeout or disconnect as soon as the camera started.
- **Solution**: We added `socketio.sleep(0)` inside the frame generation loop. This forces the server to momentarily pause and handle any pending WebSocket messages, keeping both the video and the data streams alive simultaneously.

### 4. Python Version Mismatch (MediaPipe)
- **Problem**: MediaPipe (the core of the project) is notoriously incompatible with Python 3.13. Running the project on the system's global Python caused `AttributeError` or binary load failures.
- **Solution**: We created a dedicated `server.bat` script that explicitly calls the Python 3.10 executable inside the project's virtual environment (`.\.venv\Scripts\python.exe`).

### 5. Placeholder Suppression in Speech Logic
- **Problem**: When stopping the camera, the system would sometimes speak the placeholder "Waiting for sign language input..." if no signs were detected.
- **Solution**: We added strict filtering in the `DOMContentLoaded` listener in `tab3.html` to ignore placeholder text and only trigger the speech engine if legitimate characters were recognized.

---

## 📈 Final Summary
The project now successfully bridges high-performance machine learning with a user-friendly, responsive frontend. By solving the cross-cutting issues of environment compatibility and real-time communication, HandSignify provides a seamless experience for sign language translation.
