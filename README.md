# StudySprint 📝

StudySprint is a lightweight task and productivity web application built with **Python and Flask**.  
It allows users to create, prioritize, complete, and delete tasks through a clean web interface.

This project was built to practice **object-oriented design**, **backend development**, and **real-world Git workflows**.

---

## Features

- Create tasks with priority levels (1–5)
- Mark tasks as completed
- Delete tasks
- Persistent storage using JSON (tasks remain after restart)
- User-friendly error handling with flash messages
- Clean and simple UI with priority badges

---

## Tech Stack

- **Python 3**
- **Flask**
- **HTML / CSS**
- **Pytest** (unit testing)
- **Git & GitHub**

---

## Project Structure

studysprint/
│
├── app.py # Flask application entry point
├── core/ # Core business logic
│ ├── task.py # Task model
│ └── task_manager.py # Task manager and persistence logic
├── templates/ # HTML templates
│ └── index.html
├── static/ # CSS styling
│ └── style.css
├── tests/ # Unit tests
│ └── test_task_manager.py
├── data/ # JSON storage (gitignored)
├── requirements.txt
└── README.md

---

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/keremerkoc/studysprint.git
cd studysprint
2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Run the application
python3 app.py
Open your browser at:
http://127.0.0.1:5000
Testing
Run unit tests with:
pytest
```
## Future Improvements
Add due dates and calendar view
User authentication and accounts
Database backend (SQLite or PostgreSQL)
Deployment to a cloud platform (Render, Railway, etc.)
Improved UI with a frontend framework
-----------
Author : Kerem Erkoc
