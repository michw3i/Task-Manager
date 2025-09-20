from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]}}, supports_credentials=False)


DB_NAME = 'tasks.db'

# Helper function to connect to DB
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# Add or find user
@app.route('/api/user', methods=['POST']) # This creates a POST API route at /user
def add_user():
    name = request.json.get('name') # Gets the "name" value from the request's JSON data
    conn = get_db() # Connects to the database
    c = conn.cursor()
    # Inserts name to table, ingore if name already exists
    c.execute('INSERT OR IGNORE INTO users (name) VALUES (?)', (name,))
    conn.commit()
    # Get id of the user just added (or existing user)
    c.execute('SELECT id FROM users WHERE name = ?', (name,))
    user_id = c.fetchone()['id']
    conn.close()
    return jsonify({'user_id': user_id})

@app.route('/api/task', methods=['POST'])
def add_task():
    user_id = request.json.get('user_id')
    description = request.json.get('description')
    due_date = request.json.get('due_date')
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO tasks (user_id, description, due_date) VALUES (?, ?, ?)',
                (user_id, description, due_date))
    conn.commit()
    conn.close()
    return jsonify({'status': 'Task added'})

# Get tasks for a user
@app.route('/api/tasks/<name>', methods=['GET'])
def get_user_tasks(name):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT id FROM users WHERE name = ?', (name,))
    user = c.fetchone()
    if not user:
        conn.close()
        return jsonify({'task': []})
    user_id = user['id']
    c.execute('SELECT id, description, due_date FROM tasks WHERE user_id = ?', (user_id,))
    rows = c.fetchall()
    tasks = [{'id': r['id'], 'description': r['description'], 'due_date': r['due_date']} for r in rows]
    conn.close()
    return jsonify({'name': name, 'tasks': tasks})

# Get summary of all tasks
# Delete a task
@app.route('/api/task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'Task deleted'})

@app.route('/api/summary', methods=['GET'])
def get_summary():
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        SELECT users.name, tasks.description, tasks.due_date
        FROM tasks JOIN users ON tasks.user_id = users.id
    ''')
    summary = [{'name': row['name'], 'description': row['description'], 'due_date': row['due_date']} for row in c.fetchall()]
    conn.close()
    return jsonify({'summary': summary})

# Static files serving
@app.route('/static/<path:filename>')
def serve_static(filename):
    frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    return send_from_directory(frontend_dir, filename)

# Frontend routes
@app.route('/')
def serve_frontend():
    frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    return send_from_directory(frontend_dir, 'Home.html')

@app.route('/todo')
def serve_todo():
    frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    return send_from_directory(frontend_dir, 'Todo.html')

@app.route('/financials')
def serve_financials():
    frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    return send_from_directory(frontend_dir, 'Financials.html')

@app.route('/calendar')
def serve_calendar():
    frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    return send_from_directory(frontend_dir, 'Calendar.html')


if __name__ == '__main__':
    app.run(debug=True)
