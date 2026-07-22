import { useState, useEffect } from 'react'
import './App.css'

//const API = "http://127.0.0.1:10000"
const API = "https://student-task-manager-api-3.onrender.com"

function App() {
  const [user, setUser] = useState(null)

  const [mode, setMode] = useState("login")

  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")


  const [tasks, setTasks] = useState([])
  const [input, setInput] = useState('')

  // REGISTER
  const register = () => {
    fetch(`${API}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    }).then(res => res.json())
      .then(data => {
        alert(data.message || data.error)
        if (data.message) {
          setMode("login")
        }
      })
  }

  // LOGIN
  const login = () => {
    fetch(`${API}/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",

      },
      body: JSON.stringify({
        email,
        password
      })
    }).then(res => res.json())
      .then(data => {
        if (data.token) {
          console.log("TOKEN:", data.token)
          localStorage.setItem("token", data.token)
          setUser(data.user_id)
        } else alert(data.error)
      })
  }

  // LOAD TASKS
  useEffect(() => {
    if (user) {
      fetch(`${API}/tasks`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`
        }
      })
        .then(res => res.json())
        .then(data => {
          if (Array.isArray(data)) {
            setTasks(data)
          } else {
            console.log(data)
            setTasks([])
          }
        })
    }
  }, [user])

  // ADD TASK
  const addTask = () => {
    if (!input.trim()) return

    console.log(localStorage.getItem("token"))
    fetch(`${API}/tasks`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`
      },
      body: JSON.stringify({ title: input })
    })
      .then(() => fetch(`${API}/tasks`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`
        }
      })
      )
      .then(res => res.json())
      .then(data => {
        console.log("POST RESPONSE:", data)
        if (Array.isArray(data)) {
          setTasks(data)
        } else {
          console.log(data)
          setTasks([])
        }
        setInput("")
      })
  }

  // DELETE TASK
  const deleteTask = (id) => {
    fetch(`${API}/tasks/${id}`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`
      },
      method: "DELETE"
    })
      .then(() => {
        setTasks(tasks.filter(t => t.id !== id))
      })
  }

  // TOGGLE DONE
  const toggleDone = (task) => {
    fetch(`${API}/tasks/${task.id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`
      },
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
          <h1>{mode === "login" ? "Login" : "Register"}</h1>

          <input
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <button onClick={mode === "login" ? login : register}>
            {
              mode === "login" ? "Login" : "Create account"
            }
          </button>

          <p onClick={() =>
            setMode(mode === "login" ? "register" : "login")
          } style={{ cursor: "pointer" }}>
            {
              mode === "login" ? "Create a new account" : "Already have an account? Login"
            }
          </p>

        </div>
      ) : (
        <div className="container">

          <h1 className="title">Task Manager</h1>

          <button
            className="logout"
            onClick={() => {
              setUser(null)
              localStorage.removeItem("token")
              setEmail("")
              setPassword("")
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