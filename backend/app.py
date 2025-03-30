from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

# Define Base Directories
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # backend directory
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend"))  # Move to frontend
TEMPLATES_DIR = os.path.join(FRONTEND_DIR, "templates")  # Templates folder
STATIC_DIR = os.path.join(FRONTEND_DIR, "static")  # Static folder
DB_PATH = os.path.join(BASE_DIR, "instance", "tasks.db")  # Database path

# Initialize Flask App
app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Define the Task Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    due_date = db.Column(db.String(20))
    task_time = db.Column(db.String(20))
    priority = db.Column(db.String(20))
    completed = db.Column(db.Boolean, default=False)

# Initialize the Database
with app.app_context():
    db.create_all()

# Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route('/task-tracker')
def task_tracker():
    return render_template('task_tracker.html')

@app.route('/study-tracker')
def study_tracker():
    return render_template('study_tracker.html')

@app.route('/exercise-tracker')
def exercise_tracker():
    return render_template('exercise_tracker.html')

@app.route('/food-tracker')
def food_tracker():
    return render_template('food_tracker.html')

@app.route('/selfcare-tracker')
def selfcare_tracker():
    return render_template('selfcare_tracker.html')

# API Routes for Tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([
        {"id": task.id, "name": task.name, "due_date": task.due_date, 
         "task_time": task.task_time, "priority": task.priority, "completed": task.completed}
        for task in tasks
    ])

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    new_task = Task(
        name=data['name'], due_date=data['due_date'],
        task_time=data['task_time'], priority=data['priority']
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task added successfully!"}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = not task.completed
    db.session.commit()
    return jsonify({"message": "Task updated successfully!"})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully!"})

# Run Flask App
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)



