# Copilot Instructions for Task Manager Codebase

## Big Picture Architecture
- **Backend (Python):**
  - `backend/todo.py` is a Flask API for user and task management, using SQLite (`tasks.db`).
  - `init_db.py` initializes the database schema (users, tasks tables).
  - `backend/finances.py` is experimental and not integrated with the main workflow.
- **Frontend (HTML/CSS):**
  - `frontend/` contains static HTML/CSS for Home, To-do, and Financials pages. Navigation is via `<ul class="navigation">` in each HTML file.
- **Calendar (Java):**
  - `calendar/src/App.java` is a standalone Java demo ("Hello, World!"). Not integrated with backend/frontend.

## Developer Workflows
- **Database Setup:**
  - Run `init_db.py` to create or update `tasks.db` schema before starting the backend.
- **Backend API:**
  - Start Flask app in `backend/todo.py` (default DB: `tasks.db`).
  - API endpoints:
    - `POST /user` to add/find user (`name` in JSON body).
    - `POST /task` (function exists, but not routed; see code for details).
- **Frontend Usage:**
  - Open HTML files in `frontend/` directly in browser. No build step required.
  - Navigation is static; no JS integration with backend yet.
- **Calendar App:**
  - Java code in `calendar/` is independent. Build/run with standard Java tools.

## Project-Specific Patterns & Conventions
- **Database:**
  - All tables created in `init_db.py` (run once per schema change).
  - Use `sqlite3.Row` for dict-like DB access in backend.
- **API:**
  - Flask routes use JSON for input/output.
  - User creation is idempotent (`INSERT OR IGNORE`).
- **Frontend:**
  - Navigation bar is consistent across all HTML files.
  - Forms use POST but lack JS or backend integration.
- **File Naming:**
  - Database file is `tasks.db` (not `task.db` as in some code comments).

## Integration Points
- **Backend/Frontend:**
  - No direct integration yet; future work may add JS or AJAX calls to backend API.
- **Backend/Database:**
  - All backend DB access via helper `get_db()` in `todo.py`.
- **Calendar:**
  - No integration with other components.

## Key Files & Directories
- `backend/todo.py`: Flask API, DB logic
- `init_db.py`: DB schema setup
- `frontend/`: HTML/CSS UI
- `tasks.db`: SQLite database
- `calendar/src/App.java`: Java demo

## Example: Adding a User via API
```bash
curl -X POST -H "Content-Type: application/json" -d '{"name": "Alice"}' http://localhost:5000/user
```

---

**If any section is unclear or missing important project details, please provide feedback so this guide can be improved.**
