# HabitTracker

A clean, full-stack habit tracking web application that helps you build and maintain daily routines. Design custom habits with flexible schedules, track your streaks, and visualize your progress through a weekly, monthly, or yearly calendar.

---

## Features

- **Create habits** with four frequency types: daily, weekly, monthly, or custom days of the week
- **Mark habits as complete** each day and watch your streaks grow
- **Dashboard** with at-a-glance metrics: active habits, completions today, current streaks, and all-time record
- **Calendar view** (week / month / year heatmap) showing which habits are scheduled on each day and whether they've been completed
- **Archive & delete** habits without losing their history
- **Dark / Light theme** toggle persisted to local storage
- **Auth system** — register and log in; guests can browse the landing page freely

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Angular 17 (standalone components) |
| Styling | SCSS with CSS custom properties (no Tailwind) |
| Backend | FastAPI (Python 3.11+) |
| ORM | SQLAlchemy 2 |
| Database | SQLite (file-based, zero config) |
| Validation | Pydantic v2 |
| Password hashing | bcrypt |
| Tests | pytest + httpx |

---

## Project Structure

```
HabitTracker/
├── app/                    # FastAPI backend
│   ├── main.py             # App entry point & router registration
│   ├── requirements.txt
│   └── src/
│       ├── controllers/    # Route handlers
│       ├── services/       # Business logic
│       ├── models/         # SQLAlchemy ORM models
│       └── schemas/        # Pydantic request/response schemas
│
└── frontend/               # Angular frontend
    └── src/
        └── app/
            ├── components/ # dashboard, calendar, habit-card, auth-modal
            ├── services/   # HTTP service layer
            └── models/     # TypeScript interfaces
```

---

## Getting Started

### Prerequisites

- **Python 3.11+**
- **Node.js 18+** and **npm**

---

### 1 — Backend (FastAPI)

```bash
cd app

# Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the development server
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.  
Interactive docs (Swagger UI) at `http://localhost:8000/docs`.

---

### 2 — Frontend (Angular)

Open a **new terminal**:

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

The app will open at `http://localhost:4200`.

---

### Running Tests

```bash
cd app
pytest
```

---

## API Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/users/` | Register a new user |
| `POST` | `/auth/login` | Log in |
| `GET` | `/habits/user/{user_id}` | Get all habits for a user |
| `POST` | `/habits/` | Create a habit |
| `PATCH` | `/habits/{id}` | Update a habit (title, status, etc.) |
| `DELETE` | `/habits/{id}` | Delete a habit |
| `POST` | `/habit-logs/` | Mark a habit as completed today |
| `GET` | `/habit-logs/user/{user_id}` | Get completion logs (supports date range) |
| `GET` | `/streaks/habit/{habit_id}` | Get streak data for a habit |

---

## License

MIT
