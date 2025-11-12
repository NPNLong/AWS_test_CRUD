from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DB_FILE = 'people.db'

# Khởi tạo DB nếu chưa có
def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE people (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                avatar_url TEXT
            )
        ''')
        # Thêm vài người mẫu
        cursor.executemany(
            "INSERT INTO people (name, avatar_url) VALUES (?, ?)",
            [
                ("Alice", "https://i.pravatar.cc/100?img=1"),
                ("Bob", "https://i.pravatar.cc/100?img=2"),
                ("Charlie", "https://i.pravatar.cc/100?img=3")
            ]
        )
        conn.commit()
        conn.close()

init_db()

def get_conn():
    return sqlite3.connect(DB_FILE)

@app.route("/people", methods=["GET"])
def get_people():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM people")
    rows = cursor.fetchall()
    conn.close()
    data = [{"id": r[0], "name": r[1], "avatar_url": r[2]} for r in rows]
    return jsonify(data)

@app.route("/people", methods=["POST"])
def add_person():
    data = request.json
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO people (name, avatar_url) VALUES (?, ?)",
                   (data["name"], data.get("avatar_url", "")))
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"}), 201

@app.route("/people/<int:person_id>", methods=["PUT"])
def update_person(person_id):
    data = request.json
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("UPDATE people SET name=?, avatar_url=? WHERE id=?",
                   (data["name"], data.get("avatar_url", ""), person_id))
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})

@app.route("/people/<int:person_id>", methods=["DELETE"])
def delete_person(person_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM people WHERE id=?", (person_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
