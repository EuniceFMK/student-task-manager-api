import { useState } from 'react'
import './App.css'
import { useEffect } from 'react'
function App() {
  const [tasks, setTasks] = useState([])
  const [input, setInput] = useState('')
  useEffect(() => {
    const saved = localStorage.getItem('tasks')
    if (saved) {
      setTasks(JSON.parse(saved))
    }
  }, [])
  useEffect(() => {
    localStorage.setItem('tasks', JSON.stringify(tasks))
  }, [tasks])
  const addTask = () => {
    if (input.trim() === '') return
    setTasks([...tasks, { text: input, done: false }])
    setInput('')
  }

  const deleteTask = (indexToDelete) => {
    setTasks(tasks.filter((_, index) => index !== indexToDelete))
  }

  const toggleDone = (indexToToggle) => {
    const updated = tasks.map((task, index) =>
      index === indexToToggle
        ? { ...task, done: !task.done }
        : task
    )
    setTasks(updated)
  }

  return (
    <div style={{ padding: 20 }}>
      <h1>Task Manager</h1>

      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Enter a task"
      />

      <button onClick={addTask}>Add</button>

      <ul>
        {tasks.map((task, index) => (
          <li key={index} style={{ marginTop: 10 }}>

            <span
              onClick={() => toggleDone(index)}
              style={{
                cursor: 'pointer',
                textDecoration: task.done ? 'line-through' : 'none'
              }}
            >
              {task.text}
            </span>

            <button onClick={() => deleteTask(index)} style={{ marginLeft: 10 }}>
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default App