# HandSignify: AI-Powered Sign Language Detection

HandSignify is a professional web application that uses computer vision and machine learning (MediaPipe and Random Forest) to detect and translate sign language gestures in real-time.

## 🚀 Key Features
- **Real-Time Detection**: Capture gestures via webcam with instant feedback.
- **Academic Focused**: Designed for research and professional use-cases.
- **Robust Authentication**: Secure user login and registration system.
- **Clean Architecture**: Separated logic for models, scripts, and web server.

## 🛠️ Tech Stack
- **Backend**: Flask (Python)
- **Frontend**: HTML5, Vanilla CSS, JavaScript
- **ML/CV**: OpenCV, MediaPipe, Scikit-Learn

## 📁 Project Structure
```text
project_root/
├── app.py              # Main Flask application entry point
├── manage_server.py    # Server management utility
├── server.bat          # Easy start/stop script for Windows
├── setup_project.bat   # ONE-CLICK setup script for Windows [NEW]
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── models/             # Pre-trained models and data pickles
├── scripts/            # Training, collection, and test utilities
├── static/             # CSS, JS, and image assets
├── templates/          # HTML templates
└── data/               # Processed data storage
```

## ⚙️ Setup Instructions

### 1. Clone the Repository
```powershell
git clone https://github.com/SarveshVeshi/final-year-project-of-diploma.git
cd final-year-project-of-diploma
```

### 2. Automatic Setup (Windows)
Simply run the setup script to create a virtual environment, install dependencies, and configure your environment:
```powershell
./setup_project.bat
```

### 3. Manual Setup (Optional)
If you prefer manual setup:
```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

## 🚀 Running the Project

### Start the Server
Use the provided batch script for easy control:
```powershell
./server.bat start
```
The application will be available at `http://127.0.0.1:5000`.

### Stop the Server
```powershell
./server.bat stop
```

## 🧪 Training & Utilities
Scripts for data collection and model training are located in the `scripts/` directory.

- **Collect Data**: `python scripts/collect_imgs.py`
- **Create Dataset**: `python scripts/create_dataset.py`
- **Train Model**: `python scripts/train_classifier.py`

## 🛠️ Troubleshooting
- **Port Conflict**: If port 5000 is occupied, you can change it in `app.py`.
- **MediaPipe Errors**: Ensure your camera is not being used by another application.
- **Dependency Issues**: Run `pip install --upgrade -r requirements.txt`.

## 🤝 Contributing
Feel free to open an issue or submit a pull request if you have suggestions.

---
© 2026 HandSignify.
