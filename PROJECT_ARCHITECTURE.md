# Project Architecture

## Overview
This document provides a detailed overview of the architecture of the project, including its backend, frontend, machine learning components, and database interactions.

---

## Architecture Summary

### Backend Framework
- **Flask**: The backend is built using Flask, a lightweight WSGI web application framework.

### Frontend Framework
- **Static Assets**: The frontend consists of HTML templates and static files (CSS, JavaScript) served by Flask.

### Machine Learning Components
- **Mediapipe**: Used for hand tracking and gesture recognition.
- **OpenCV**: Used for image and video processing.
- **Scikit-learn**: Used for classification tasks.

### Database
- **Flask-SQLAlchemy**: Used for ORM and database interactions. Likely connected to SQLite or PostgreSQL.

### Microservices
- **Sign Language Service**: Located in `services/sign_service.py`, handles sign language-related operations.

---

## Data Flow
1. **Frontend**:
   - User interacts with the frontend through HTML templates and static assets.
   - Requests are sent to the backend via HTTP.

2. **Backend**:
   - Flask routes handle requests and process data.
   - Interacts with the database using Flask-SQLAlchemy.
   - Performs ML inference using Mediapipe and OpenCV.

3. **Database**:
   - Stores user data and application state.

4. **Machine Learning**:
   - Processes video/image data for sign language recognition.

---

## API Routes
- **Defined in `app.py`**:
  - `/home`: Renders the home page.
  - `/feed`: Displays the feed.
  - `/sign_text_converter`: Converts text to sign language.
  - `/voice_converter`: Converts voice to text.

---

## WebSocket Connections
- **Flask-SocketIO**: Used for real-time communication.

---

## Model Inference Pipeline (Cloud-Compatible)
1. **Frontend**: The browser captures video via `navigator.mediaDevices.getUserMedia`.
2. **Local Detection**: MediaPipe JS extracts 21 hand landmarks directly in the browser.
3. **API Call**: Landmarks are sent to the `/api/predict` endpoint in `app.py`.
4. **Backend Classification**: The Flask server uses the pre-trained Random Forest model (`model.p`) to classify the landmarks.
5. **Real-Time Update**: The prediction is returned to the frontend and displayed instantly.

---

## ☁️ Cloud Deployment (Vercel/Global)
The architecture is now optimized for public cloud platforms. By offloading camera hardware access to the user's browser, the application no longer requires a physical webcam on the server, making it compatible with Vercel, Heroku, and other cloud providers.

## Frontend-Backend Interaction
- Flask renders templates and serves static files.
- API endpoints handle dynamic data requests.

---

## State Management
- **Flask-Login**: Manages user sessions.

---

## Event Emission System
- **Flask-SocketIO**: Handles real-time events.