from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DB_NAME = 'tasks.db'

# Helper function to connect to DB
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# Add or find user
@app.route('/user', methods=['POST']) # This creates a POST API route at /user
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

@app.route('/task', methods=['POST'])
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
@app.route('/tasks/<name>', methods=['GET'])
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
@app.route('/task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'Task deleted'})

@app.route('/summary', methods=['GET'])
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

@app.route('/')
def home():
    return 'Welcome to the Task Manager API. Use /user, /task, /tasks/<name>, or /summary.'


if __name__ == '__main__':
    app.run(debug=True)

    