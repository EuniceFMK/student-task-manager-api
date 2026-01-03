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
 
app = Flask (__name__) #Create my flask application / app= my web server

#List of tasks / Each task is a dictionnary (object)
tasks = [
    {"id":1,"title":"Study Python", "done": False},
    {"id": 2, "title": "Build Flask API", "done": False}
]

# GET = Read Data / @app.route relate a URL with a Python function
@app.route("/tasks", methods=["GET"])    # This line transform the python script in API REST
def get_tasks():  #backend function
    return jsonify(tasks)      #transform the python list in JSON

#POST = Add Data
@app.route("/tasks",methods=["POST"])
def add_task():
    data=request.get_json()
    
    new_task ={
        "id" :len(tasks)+1,
        "title": data.get("title"),
        "done":False
    }

    tasks.append(new_task)
    return jsonify(new_task),201

#PUT = Update Data
@app.route ("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data= request.get_json()
    for task in tasks:
        if task ["id"] == task_id:
            task ["title"]= data.get("title",task["title"])
            task ["done"]= data.get("done",task ["done"])
            return jsonify(task)
    return jsonify({"error":"Task not found"}), 404

#DELETE = Delete Data
@app.route ("/tasks/<int:task_id>",methods=["DELETE"])
def delete_task(task_id):
    for task in tasks:
        if task["id"]== task_id:
            tasks.remove(task)
            return jsonify({"message":"Task deleted"})
    return jsonify ({"error":"Task not found"}),404

if __name__ == "__main__":   #Does the file executed directly?
    app.run(debug=True)   

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