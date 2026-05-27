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

app = Flask (__name__) #Create my flask application / app= my web server
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)

@app.route("/")
def home():
    return "Student Task Manager API is running"

# GET = Read Data / @app.route relate a URL with a Python function
@app.route("/tasks", methods=["GET"])    # This line transform the python script in API REST
def get_tasks():  #backend function
   all_tasks = Task.query.all()  
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
def add_task():
    data = request.get_json()
    if not data or not data.get("title"):
     return jsonify({"error": "Title is required"}), 400
    new_task = Task(
        title=data.get("title"),
        done=False
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