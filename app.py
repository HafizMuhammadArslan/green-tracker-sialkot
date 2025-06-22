from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

DB_NAME = 'trees.db'

# 1. Create database and table if not exist
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            species TEXT,
            planted_by TEXT,
            location TEXT,
            date_planted TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

# 2. Homepage route (serves your HTML)
@app.route('/')
def home():
    return render_template('index.html')

# 3. Add new tree
@app.route('/tree', methods=['POST'])
def add_tree():
    data = request.get_json()
    print("Received:", data)  # debug message
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO trees (species, planted_by, location, date_planted, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        data['species'],
        data['planted_by'],
        data['location'],
        data['date_planted'],
        data['status']
    ))
    conn.commit()
    conn.close()
    return jsonify({"message": "Tree added"}), 201

# 4. Show all trees
@app.route('/trees', methods=['GET'])
def get_trees():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM trees")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([
        {
            "id": row[0],
            "species": row[1],
            "planted_by": row[2],
            "location": row[3],
            "date_planted": row[4],
            "status": row[5]
        } for row in rows
    ])

# 5. Delete a tree
@app.route('/tree/<int:id>', methods=['DELETE'])
def delete_tree(id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM trees WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Tree deleted"})

# 6. Run the app
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
