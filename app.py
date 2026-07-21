# def add_task(title):
#     return {"title":title,"done":False}

# tasks = []
# tasks.append ("Finish assignment")

# task = {
#     "id":1,
#     "title":"Study Python",
#     "done":False
# }

# for task in tasks:
#     print(task)

#pip install flask --To run the Flask
from flask import Flask, jsonify, request    #Flask -- Class to create a web app/ jsonify is used for my app to speak web language
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask (__name__) #Create my flask application / app= my web server
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "student-task-manager-secret-key"  # Change this to a random secret key in production

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

class User(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   email = db.Column(db.String(120), unique=True, nullable=False)
   password = db.Column(db.String(200), nullable=False)
   tasks = db.relationship("Task", backref="owner", lazy=True)

@app.route("/")
def home():
    return "Student Task Manager API is running"

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    email = email.lower()
    password = data.get("password")
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400
    
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = User(email=email, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    email = email.lower()
    password = data.get("password")
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401
    
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password"}), 401
    
    token = create_access_token(identity=user.id)
    return jsonify({
        "message": "Login successful",
        "token": token,
        "user_id": user.id
        }), 200

# GET = Read Data / @app.route relate a URL with a Python function
@app.route("/tasks", methods=["GET"])    # This line transform the python script in API REST
@jwt_required()
def get_tasks():  #backend function
   current_user_id = get_jwt_identity()
   all_tasks = Task.query.filter_by(user_id=current_user_id).all()
   result = []
   for task in all_tasks:
    result.append({
        "id": task.id,
        "title": task.title,
        "done": task.done
    })
   return jsonify(result)

#POST = Add Data
@app.route("/tasks",methods=["POST"])
@jwt_required()
def add_task():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    if not data or not data.get("title"):
     return jsonify({"error": "Title is required"}), 400
    new_task = Task(
        title=data.get("title"),
        done=False,
        user_id=current_user_id
    )

    db.session.add(new_task)
    db.session.commit()

    return jsonify({
        "id": new_task.id,
        "title": new_task.title,
        "done": new_task.done
    }), 201

#PUT = Update Data
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):

    task = Task.query.get(task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()

    task.title = data.get("title", task.title)
    task.done = data.get("done", task.done)

    db.session.commit()

    return jsonify({
        "id": task.id,
        "title": task.title,
        "done": task.done
    })

#DELETE = Delete Data
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):

    task = Task.query.get(task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Task deleted"})

with app.app_context():
    db.create_all()
    print("Database tables created!")
    
if __name__ == "__main__":   #Does the file executed directly?
    app.run(host="0.0.0.0", port=10000, debug=True)

# fetch("http://127.0.0.1:5000/tasks", {
#   method: "POST",
#   headers: {
#     "Content-Type": "application/json"
#   },
#   body: JSON.stringify({
#     title: "Prepare IBM application"
#   })
# })
# .then(response => response.json())
# .then(data => console.log(data));
#https://student-task-manager-api-04mv.onrender.com/tasks  Deployment link