from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os


# Define Base Directories
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend"))  
TEMPLATES_DIR = os.path.join(FRONTEND_DIR, "templates")  
STATIC_DIR = os.path.join(FRONTEND_DIR, "static")  
DB_PATH = os.path.join(BASE_DIR, "instance", "tasks.db")  

# Initialize Flask App
app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)
app.secret_key = "your_secret_key"  # Required for session management

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Define the User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    pin = db.Column(db.String(6))  # For 6-digit PIN login
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))

# Define the Task Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    due_date = db.Column(db.String(20))
    task_time = db.Column(db.String(20))
    priority = db.Column(db.String(20))
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Initialize the Database
with app.app_context():
    db.create_all()

# Routes
@app.route("/")
def home():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("index.html", logged_in=session.get("logged_in"), username=session.get("username"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("logged_in"):
        return redirect(url_for("home"))
        
    if request.method == "POST":
        auth_method = request.form.get("auth_method")
        
        if auth_method == "username":
            username = request.form.get("username")
            password = request.form.get("password")
            
            user = User.query.filter_by(username=username).first()
            
            if user and check_password_hash(user.password, password):
                session["logged_in"] = True
                session["username"] = user.username
                session["user_id"] = user.id
                flash("Login successful!", "success")
                return redirect(url_for("home"))
            else:
                flash("Invalid username or password", "error")
                
        elif auth_method == "pin":
            email = request.form.get("email")
            pin = ''.join([
                request.form.get("pin1"),
                request.form.get("pin2"),
                request.form.get("pin3"),
                request.form.get("pin4"),
                request.form.get("pin5"),
                request.form.get("pin6")
            ])
            
            user = User.query.filter_by(email=email).first()
            
            if user and user.pin == pin:
                session["logged_in"] = True
                session["username"] = user.username
                session["user_id"] = user.id
                flash("PIN login successful!", "success")
                return redirect(url_for("home"))
            else:
                flash("Invalid email or PIN", "error")
    
    return render_template("auth/login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if session.get("logged_in"):
        return redirect(url_for("home"))
        
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        # Validate passwords match
        if password != confirm_password:
            flash("Passwords don't match!", "error")
            return redirect(url_for("signup"))
            
        # Check if username or email already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash("Username or email already taken!", "error")
            return redirect(url_for("signup"))
            
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        
        # Handle PIN if enabled
        enable_pin = request.form.get("enable_pin") == "on"
        pin = None
        if enable_pin:
            pin = ''.join([
                request.form.get("pin1"),
                request.form.get("pin2"),
                request.form.get("pin3"),
                request.form.get("pin4"),
                request.form.get("pin5"),
                request.form.get("pin6")
            ])
        
        # Create new user
        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
            pin=pin,
            first_name=first_name,
            last_name=last_name
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash("Registration successful! Please login.", "success")
        return redirect(url_for("login"))
    
    return render_template("auth/signup.html")

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    session.pop("username", None)
    session.pop("user_id", None)
    flash("You have been logged out", "info")
    return redirect(url_for("login"))

@app.route("/profile")
def profile():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("profile.html", username=session.get("username"))

# Protected Pages
@app.route("/task-tracker")
def task_tracker():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("task_tracker.html")

@app.route("/study-tracker")
def study_tracker():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("study_tracker.html")

@app.route("/exercise-tracker")
def exercise_tracker():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("exercise_tracker.html")

@app.route("/food-tracker")
def food_tracker():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("food_tracker.html")

@app.route("/selfcare-tracker")
def selfcare_tracker():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("selfcare_tracker.html")




# Run Flask App
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)