import { useState, useEffect } from 'react'
import './App.css'

const API = "https://student-task-manager-api-3.onrender.com"

function App() {
  const [user, setUser] = useState(null)
  const [loginInput, setLoginInput] = useState("")

  const [tasks, setTasks] = useState([])
  const [input, setInput] = useState('')

  // LOAD USER
  useEffect(() => {
    const saved = localStorage.getItem("user")
    if (saved) setUser(saved)
  }, [])

  useEffect(() => {
    if (user) {
      localStorage.setItem("user", user)
    }
  }, [user])

  // LOAD TASKS
  useEffect(() => {
    if (user) {
      fetch(`${API}/tasks`)
        .then(res => res.json())
        .then(data => setTasks(data))
    }
  }, [user])

  // ADD TASK
  const addTask = () => {
    if (!input.trim()) return

    fetch(`${API}/tasks`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: input })
    })
      .then(() => fetch(`${API}/tasks`))
      .then(res => res.json())
      .then(data => {
        setTasks(data)
        setInput('')
      })
  }

  // DELETE TASK
  const deleteTask = (id) => {
    fetch(`${API}/tasks/${id}`, { method: "DELETE" })
      .then(() => {
        setTasks(tasks.filter(t => t.id !== id))
      })
  }

  // TOGGLE DONE
  const toggleDone = (task) => {
    fetch(`${API}/tasks/${task.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ done: !task.done })
    })
      .then(res => res.json())
      .then(updated => {
        setTasks(tasks.map(t => t.id === updated.id ? updated : t))
      })
  }

  return (
    <div className="page">

      {!user ? (
        <div className="container">
          <h1>Login</h1>

          <input
            placeholder="Enter your name"
            value={loginInput}
            onChange={(e) => setLoginInput(e.target.value)}
          />

          <button onClick={() => setUser(loginInput)}>
            Login
          </button>
        </div>
      ) : (
        <div className="container">

          <h1 className="title">Task Manager</h1>

          <button
            onClick={() => {
              setUser(null)
              localStorage.removeItem("user")
            }}
          >
            Logout
          </button>
          <div className="inputBox">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Write a task..."
            />
            <button onClick={addTask}>Add</button>
          </div>


          <div className="list">
            {tasks.map(task => (
              <div className="task" key={task.id}>

                <span
                  onClick={() => toggleDone(task)}
                  className={task.done ? "done" : ""}
                >
                  {task.title}
                </span>

                <button onClick={() => deleteTask(task.id)}>
                  ✕
                </button>

              </div>
            ))}
          </div>

        </div>
      )}

    </div>
  )
}

export default App