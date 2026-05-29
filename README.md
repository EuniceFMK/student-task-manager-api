# 📌 Student Task Manager

A full-stack task management web application built with **React (frontend)** and **Flask (backend)**, featuring authentication, role-based access control, and CRUD operations for tasks.

---

## 🚀 Live Demo
### 📸 Screenshots
![Task Management Dashborad](image.png)
* Frontend (Vercel): https://student-task-manager-api-two.vercel.app/
* Backend (Render API): https://student-task-manager-api-3.onrender.com

---

## 🧠 Features

### 👤 Authentication

* Simple login system (session-based via localStorage)
* Role-based access (Root / Admin / Member)

### 📋 Task Management

* Create tasks
* View tasks
* Mark tasks as done/undone
* Delete tasks

### 🔐 Admin Panel

* User management (create, update, delete users)
* Role management system
* Assign roles to users

---

## 🛠️ Tech Stack

### Frontend

* React
* Vite
* JavaScript
* CSS

### Backend

* Flask
* Flask-CORS
* Python
* MySQL / SQLite (depending on setup)

### Deployment

* Vercel (Frontend)
* Render (Backend API)
* GitHub (Version Control)

---

## 📁 Project Structure

```
student-task-manager/
│
├── task-manager-frontend/
│   ├── App.jsx
│   ├── main.jsx
│   └── styles/
│
├── app.py
├── db.py
└── routes/
```

---

## ⚙️ Setup (Local Development)

### 1. Clone repository

```bash
git clone https://github.com/EuniceFMK/student-task-manager-api.git
```

### 2. Backend setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### 3. Frontend setup

```bash
cd frontend
npm install
npm run dev
```

---

## 🌐 API Endpoints

| Method | Endpoint   | Description        |
| ------ | ---------- | ------------------ |
| GET    | /tasks     | Get all tasks      |
| POST   | /tasks     | Add new task       |
| PUT    | /tasks/:id | Update task status |
| DELETE | /tasks/:id | Delete task        |

---

## 🔒 Roles System

| Role   | Permissions                         |
| ------ | ----------------------------------- |
| Root   | Full access (users + roles + tasks) |
| Admin  | Manage users + tasks                |
| Member | Manage own tasks                    |

---

## ✨ Future Improvements

* JWT authentication
* Password encryption improvements
* Pagination for tasks
* UI improvements
* Database migration to PostgreSQL

---

## 👩🏽‍💻 Author

Built by **Eunice**
Computer Engineering Technology Student @ NAIT

---

## 📌 Note

This project was built for learning purposes (school lab) and demonstrates full-stack development, authentication, and deployment skills.
