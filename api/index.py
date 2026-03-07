# I am using mediapipe as a hand landmark processing and prediction and landmark detector and a Random Forest classifier as sign classifier.


from flask import Flask, jsonify, render_template, url_for, redirect, flash, session, request, Response
import sys
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from flask_socketio import SocketIO, emit
import socketio
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, Email, EqualTo
from flask_bcrypt import Bcrypt
from datetime import datetime
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from flask_mail import Message, Mail
import os
import random
import re
import pickle
try:
    import cv2
    import mediapipe as mp
    from mediapipe.python import solutions as mp_solutions
    HAS_CAMERA_DEPS = True
except ImportError:
    HAS_CAMERA_DEPS = False
import numpy as np
from services.sign_service import sign_service

from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.github import make_github_blueprint, github
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__, 
            template_folder='../templates', 
            static_folder='../static')

CORS(app)  # Allow cross-origin requests for all routes

# -------------------Encrypt Password using Hash Func-------------------
bcrypt = Bcrypt(app)

# -------------------Database Model Setup-------------------
# Use absolute path for SQLite to work from api/ folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJ_DIR = os.path.dirname(BASE_DIR)
SQLITE_PATH = os.path.join(PROJ_DIR, 'database.db')

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', f'sqlite:///{SQLITE_PATH}')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'thisisasecretkey')
serializer = Serializer(app.config['SECRET_KEY'])
db = SQLAlchemy(app)
# app.app_context().push() # Removing push() for cleaner serverless execution

# -------------------Socket.IO Setup-------------------
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# -------------------mail configuration-------------------
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER", 'smtp.gmail.com')
app.config["MAIL_PORT"] = int(os.environ.get("MAIL_PORT", 587))
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME", 'handssignify@gmail.com')
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD", 'ttbylakctxvvvnxe')
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS", 'True') == 'True'
app.config["MAIL_USE_SSL"] = os.environ.get("MAIL_USE_SSL", 'False') == 'True'
mail = Mail(app)

# -------------------OAuth Configuration-------------------
# Set environment variable to allow HTTP for local development
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Google OAuth
google_bp = make_google_blueprint(
    client_id=os.environ.get('GOOGLE_CLIENT_ID'),
    client_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
    scope=['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'],
    redirect_url='/oauth/google/callback'
)
app.register_blueprint(google_bp, url_prefix='/login')

# GitHub OAuth
github_bp = make_github_blueprint(
    client_id=os.environ.get('GITHUB_CLIENT_ID'),
    client_secret=os.environ.get('GITHUB_CLIENT_SECRET'),
    redirect_url='/oauth/github/callback'
)
app.register_blueprint(github_bp, url_prefix='/login')
# --------------------------------------------------------


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# -------------------Database Model-------------------


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(80), nullable=True)  # Nullable for OAuth users
    oauth_provider = db.Column(db.String(20), nullable=True)  # 'google', 'github', 'facebook'
    oauth_id = db.Column(db.String(100), nullable=True, unique=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
# ----------------------------------------------------

# -------------------Intro & Home Pages-------------------
@app.route("/")
def intro():
    return render_template("intro.html")

@app.route("/home")
def home():
    return render_template("home.html")
# ----------------------------------------------------

# -------------------OAuth Callback Routes-------------------

@app.route('/oauth/google/callback')
def google_callback():
    if not google.authorized:
        flash('Google login failed.', 'danger')
        return redirect(url_for('login'))
    resp = google.get('/oauth2/v2/userinfo')
    if not resp.ok:
        flash('Failed to fetch Google user info.', 'danger')
        return redirect(url_for('login'))
    info = resp.json()
    oauth_id = 'google_' + str(info.get('id', ''))
    email = info.get('email', '')
    name = info.get('name', email.split('@')[0])
    return _oauth_login_or_register(oauth_id, 'google', name, email)


@app.route('/oauth/github/callback')
def github_callback():
    if not github.authorized:
        flash('GitHub login failed.', 'danger')
        return redirect(url_for('login'))
    resp = github.get('/user')
    if not resp.ok:
        flash('Failed to fetch GitHub user info.', 'danger')
        return redirect(url_for('login'))
    info = resp.json()
    oauth_id = 'github_' + str(info.get('id', ''))
    name = info.get('login', 'github_user')
    email = info.get('email', '') or f"{name}@github.oauth"
    return _oauth_login_or_register(oauth_id, 'github', name, email)


def _oauth_login_or_register(oauth_id, provider, username, email):
    """Find or create a user from OAuth and log them in."""
    user = User.query.filter_by(oauth_id=oauth_id).first()
    if user:
        # Existing OAuth user — log them in
        login_user(user)
        session['name'] = user.username
        session['logged_in'] = True
        flash(f'Welcome back, {user.username}!', 'success')
        return redirect(url_for('home'))
    else:
        # New OAuth user — create account
        # Ensure unique username
        base_username = username[:25]
        final_username = base_username
        counter = 1
        while User.query.filter_by(username=final_username).first():
            final_username = f"{base_username}_{counter}"
            counter += 1
        new_user = User(
            username=final_username,
            email=email[:30],
            password=bcrypt.generate_password_hash(os.urandom(24).hex()).decode('utf-8'),
            oauth_provider=provider,
            oauth_id=oauth_id
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        session['name'] = new_user.username
        session['logged_in'] = True
        flash(f'Account created via {provider.title()}! Welcome, {new_user.username}!', 'success')
        return redirect(url_for('home'))
# --------------------------------------------------------

# -------------------feed back Page-----------------------
@app.route('/feed', methods=['GET', 'POST'])
def feed():
    return render_template('feed.html')
# ----------------------------------------------------


# -------------------Discover More Page---------------
@app.route('/discover_more', methods=['GET', 'POST']) 
def discover_more():
    return render_template('discover_more.html')
# ----------------------------------------------------

# -------------------Guide Page-----------------------
@app.route('/guide', methods=['GET', 'POST'])
def guide():
    return render_template('guide.html')
# ----------------------------------------------------


# ------------------- New Split Navigation Pages -------------------

# Tab 1: Sign → Text (Sign-Text)
@app.route('/tab-1', methods=['GET'])
def tab_1():
    name = session.get('name', 'Guest')
    return render_template('sign_text_converter.html', name=name, active_panel='signToTextPanel')

# Tab 2: Text → Sign (Text-Sign)
@app.route('/tab-2', methods=['GET'])
def tab_2():
    return render_template('sign_text_converter.html', active_panel='textToSignPanel')

# Tab 3: Sign → Voice (Sign-Voice)
@app.route('/tab-3', methods=['GET'])
def tab_3():
    name = session.get('name', 'Guest')
    return render_template('sign_text_converter.html', name=name, active_panel='voiceToSignPanel')

# Tab 4: Voice → Sign (Voice-Sign)
@app.route('/tab-4', methods=['GET'])
def tab_4():
    return render_template('sign_text_converter.html', active_panel='signToVoicePanel')

@app.route('/sign-language', methods=['GET'])
def sign_language():
    # Old generate route - redirect to the new text-to-sign tab
    flash('This page has moved! Redirecting to Text-to-Sign converter.', 'info')
    return redirect(url_for('tab_2'))

@app.route('/generate_sign_video_api', methods=['POST'])
def generate_sign_video_api():
    data = request.get_json()
    text = data.get('text')
    language = data.get('language', 'ASL')
    
    result = sign_service.generate_sign_video(text, language)
    return jsonify(result)

@app.route('/get_sign_images', methods=['POST'])
def get_sign_images():
    data = request.get_json()
    text = data.get('text', '')
    language = data.get('language', 'ASL')
    
    image_paths = sign_service.get_sign_images_from_text(text, language)
    return jsonify({"success": True, "image_paths": image_paths})
# ----------------------------------------------------

@app.route('/sign_text_converter', methods=['GET'])
def sign_text_converter():
    name = session.get('name', 'Guest')
    active_panel = request.args.get('panel', 'signToTextPanel')
    return render_template('sign_text_converter.html', name=name, active_panel=active_panel)

@app.route('/voice_converter', methods=['GET'])
def voice_converter():
    return render_template('voice_converter.html')

# --------------------Login Page-------------------
class LoginForm(FlaskForm):
    email = StringField(label='email', validators=[InputRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField(label='password', validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # Check if the user has registered before showing the login form
    if 'registered' in session and session['registered']:
        session.pop('registered', None)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successfully.', category='success')
            session['name'] = user.username
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            flash(f'Login unsuccessful for {form.email.data}. Check email and password.', category='danger')
    return render_template('login.html', form=form)
# ----------------------------------------------------


# -------------------Dashboard or Logged Page-------------------
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    name = session.get('name', 'Tester')
    return render_template('dashboard.html', name=name)
# ----------------------------------------------------

# -------------------About Page-----------------------
@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')
# ----------------------------------------------------

# -------------------Logged Out Page-------------------

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    session.clear()
    logout_user()
    flash('Account Logged out successfully.', category='success')
    return redirect(url_for('login'))
# ----------------------------------------------------

# -------------------Register Page-------------------

class RegisterForm(FlaskForm):
    username = StringField(label='username', validators=[InputRequired()], render_kw={"placeholder": "Username"})
    email = StringField(label='email', validators=[InputRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField(label='password', validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField(label='confirm_password', validators=[InputRequired(), EqualTo('password')], render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            flash('That Username already exists. Please choose a different one.', 'danger')
            raise ValidationError('That username already exists. Please choose a different one.')


@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        # Log the user in immediately
        login_user(new_user)
        session['name'] = new_user.username
        session['logged_in'] = True
        
        flash(f'Account Created for {form.username.data} successfully! Welcome!', category='success')
        return redirect(url_for('home'))

    return render_template('register.html', form=form)
# ----------------------------------------------------

# -------------------Update or reset Email Page-------------------


class ResetMailForm(FlaskForm):
    username = StringField(label='username', validators=[InputRequired()], render_kw={"placeholder": "Username"})
    email = StringField(label='email', validators=[InputRequired(), Email()], render_kw={"placeholder": "Old Email"})
    new_email = StringField(label='new_email', validators=[InputRequired(), Email()], render_kw={"placeholder": "New Email"})
    password = PasswordField(label='password', validators=[InputRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login', validators=[InputRequired()])


@app.route('/reset_email', methods=['GET', 'POST'])
@login_required
def reset_email():
    form = ResetMailForm()
    if 'logged_in' in session and session['logged_in']:
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data) and User.query.filter_by(email=form.email.data).first():
                user.email = form.new_email.data  # Replace old email with new email
                db.session.commit()
                flash('Email reset successfully.', category='success')
                session.clear()
                return redirect(url_for('login'))
            else:
                flash('Invalid email, password, or combination.', category='danger')

        return render_template('reset_email.html', form=form)
    return redirect(url_for('login'))
# --------------------------------------------------------------

# -------------------Forgot Password With OTP-------------------

class ResetPasswordForm(FlaskForm):
    username = StringField(label='username', validators=[InputRequired()], render_kw={"placeholder": "Username"})
    email = StringField(label='email', validators=[InputRequired(), Email()], render_kw={"placeholder": "Email"})
    submit = SubmitField('Submit', validators=[InputRequired()])


class ForgotPasswordForm(FlaskForm):
    username = StringField(label='username', validators=[InputRequired()], render_kw={"placeholder": "Username"})
    email = StringField(label='email', validators=[InputRequired(), Email()], render_kw={"placeholder": "Email"})
    new_password = PasswordField(label='new_password', validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "New Password"})
    confirm_password = PasswordField(label='confirm_password', validators=[InputRequired(), EqualTo('new_password')], render_kw={"placeholder": "Confirm Password"})
    otp = StringField(label='otp', validators=[InputRequired(), Length(min=6, max=6)], render_kw={"placeholder": "Enter OTP"})
    submit = SubmitField('Submit', validators=[InputRequired()])


@staticmethod
def send_mail(name, email, otp):
    msg = Message('Reset Email OTP Password',sender='handssignify@gmail.com', recipients=[email])
    msg.body = "Hii " + name + "," + "\nYour email OTP is :"+str(otp)
    mail.send(msg)


    # Generate your OTP logic here
def generate_otp():
    return random.randint(100000, 999999)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    otp = generate_otp()
    session['otp'] = otp
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and User.query.filter_by(email=form.email.data).first():
            send_mail(form.username.data, form.email.data, otp)
            flash('Reset Request Sent. Check your mail.', 'success')
            return redirect(url_for('forgot_password'))
        else:
            flash('Email and username combination is not exist.', 'danger')
    return render_template('reset_password_request.html', form=form)


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        otp = request.form['otp']
        valid = (otp == request.form['otp'])

        if valid:
            user = User.query.filter_by(username=form.username.data).first()
            if user and User.query.filter_by(email=form.email.data).first():
                user.password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
                db.session.commit()
                flash('Password Changed Successfully.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Email and username combination is not exist.', 'danger')
        else:
            flash("OTP verification failed.", 'danger')
    return render_template('forgot_password.html', form=form)
# ---------------------------------------------------------------

# ------------------------- Update Password ---------------------

class UpdatePasswordForm(FlaskForm):
    username = StringField(label='username', validators=[InputRequired()], render_kw={"placeholder": "Username"})
    email = StringField(label='email', validators=[InputRequired(), Email()], render_kw={"placeholder": "Email"})
    new_password = PasswordField(label='new_password', validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "New Password"})
    confirm_password = PasswordField(label='confirm_password', validators=[InputRequired(), EqualTo('new_password')], render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Submit', validators=[InputRequired()])


@app.route('/update_password', methods=['GET', 'POST'])
@login_required
def update_password():
    form = UpdatePasswordForm()
    if form.validate_on_submit() and 'logged_in' in session and session['logged_in']:

            user = User.query.filter_by(username=form.username.data).first()
            if user and User.query.filter_by(email=form.email.data).first():
                user.password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
                db.session.commit()
                flash('Password Changed Successfully.', 'success')
                session.clear()
                return redirect(url_for('login'))
            else:
                flash("Username and email combination is not exist.", 'danger')
    return render_template('update_password.html', form=form)
# -----------------------------  end  ---------------------------


# ------------------------- Data Refinement ---------------------
def refine_text(raw_text: str) -> str:
    """
    Deterministic cleaning logic for recognized sign language text.
    """
    if not raw_text:
        return ""
    
    # 1. Split text into words using whitespace
    words = raw_text.split()
    
    # 2. Remove single-letter noise except "I", "A"
    valid_single_letters = {"I", "A"}
    cleaned_words = []
    for word in words:
        upper_word = word.upper().replace('.', '').replace(',', '')
        if len(upper_word) > 1 or upper_word in valid_single_letters:
            cleaned_words.append(word)
            
    # 3. Remove consecutive duplicate words
    # 4. Remove excessive repetition (max 2 consecutive occurrences rule simplified to 1 for clarity)
    final_words = []
    for word in cleaned_words:
        if not final_words or word != final_words[-1]:
            final_words.append(word)
            
    # 5 & 6. Join back into a clean sentence
    return " ".join(final_words)

@socketio.on('refine_text')
def handle_refine_text(data):
    raw_text = data.get('text', '')
    refined = refine_text(raw_text)
    emit('refined_text_update', {'refined_text': refined})

# -----------------------------  end  ---------------------------

# --------------------------- Machine Learning ------------------
import os
import pickle

# Robust path handling for Vercel/Production
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'model.p')

try:
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, 'rb') as f:
            model_dict = pickle.load(f)
        model = model_dict['model']
    else:
        print(f"Model file not found at {MODEL_PATH}")
        model = None
except Exception as e:
    print("Error loading the model:", e)
    model = None
@app.route('/generate_frames', methods=['POST'])
def generate_frames():
    sys.stderr.write("DEBUG: generate_frames called\n")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        sys.stderr.write("DEBUG: Failed to open camera\n")
    else:
        sys.stderr.write("DEBUG: Camera opened successfully\n")
    
    mp_hands = mp_solutions.hands
    mp_drawing = mp_solutions.drawing_utils
    mp_drawing_styles = mp_solutions.drawing_styles

    hands = mp_hands.Hands(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
    
    last_emitted_char = None

    labels_dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M',
               13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z', 26: 'Hello', 27: 'Done', 28: 'Thank You', 29: 'I Love you', 30: 'Sorry', 31: 'Please', 32: 'You are welcome.' }

    try:
        while True:
            data_aux = []
            x_ = []
            y_ = []

            ret, frame = cap.read()
            if not ret:
                sys.stderr.write("DEBUG: Failed to read frame\n")
                break
            
            H, W, _ = frame.shape
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            try:
                results = hands.process(frame_rgb)
            except Exception as e:
                sys.stderr.write(f"DEBUG: Mediapipe error: {e}\n")
                continue

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())

                # ... Rest of the hand landmark processing and prediction code ...
                data_aux = []
                x_ = []
                y_ = []

                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y

                    x_.append(x)
                    y_.append(y)

                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    data_aux.append(x - min(x_))
                    data_aux.append(y - min(y_))

                x1 = int(min(x_) * W) - 10
                y1 = int(min(y_) * H) - 10

                x2 = int(max(x_) * W) - 10
                y2 = int(max(y_) * H) - 10

                try:
                    prediction = model.predict([np.asarray(data_aux)])
                    predicted_character = labels_dict[int(prediction[0])]
                    
                    if predicted_character != last_emitted_char:
                        # Only emit on change to reduce traffic
                        socketio.emit('prediction', {'character': predicted_character}, namespace='/')
                        socketio.emit('stable_prediction', {'character': predicted_character}, namespace='/')
                        last_emitted_char = predicted_character
                    
                    # Yield to event loop to keep WebSocket alive
                    socketio.sleep(0)

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
                    cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,cv2.LINE_AA)
                    # flash(f'Predicted Character is {predicted_character}.', category='success')

                except Exception as e:
                       pass
                       #print(e)
                       # Handle prediction error

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    finally:
        sys.stderr.write("DEBUG: Releasing camera\n")
        cap.release()

@app.route('/video_feed')
def video_feed():
    if not HAS_CAMERA_DEPS:
        return "Camera processing is not available in cloud deployment. Please use the client-side camera features.", 501
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# --------------------------- Prediction API ------------------

@app.route('/api/predict', methods=['POST'])
def predict_landmarks():
    """
    API endpoint that accepts hand landmarks and returns a prediction.
    Enables cloud deployment by offloading camera capture to the browser.
    """
    data = request.get_json()
    if not data or 'landmarks' not in data:
        return jsonify({"success": False, "error": "No landmarks provided"}), 400
    
    landmarks_raw = data['landmarks'] # Expected to be a list of 21 {x, y, z} dicts
    
    if model is None:
        return jsonify({"success": False, "error": "Model not loaded on server"}), 500

    try:
        data_aux = []
        x_ = []
        y_ = []

        # Extract x and y coordinates
        for lm in landmarks_raw:
            x_.append(lm['x'])
            y_.append(lm['y'])

        # Normalize landmarks relative to the minimum x and y (as required by the model)
        for lm in landmarks_raw:
            data_aux.append(lm['x'] - min(x_))
            data_aux.append(lm['y'] - min(y_))

        # Perform prediction
        prediction = model.predict([np.asarray(data_aux)])
        
        labels_dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M',
                   13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z', 26: 'Hello', 27: 'Done', 28: 'Thank You', 29: 'I Love you', 30: 'Sorry', 31: 'Please', 32: 'You are welcome.' }
        
        predicted_character = labels_dict[int(prediction[0])]
        
        return jsonify({
            "success": True, 
            "character": predicted_character
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# -----------------------------  end  ---------------------------

if __name__ == '__main__':
    socketio.run(app, debug=True, use_reloader=False, port=5001)
