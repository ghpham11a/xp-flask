from flask import Blueprint, request, jsonify
from . import db
import os

bp = Blueprint("user", __name__)

@bp.route("/user", methods=["POST"])
def create_user():
    new_todo = request.json
    name = new_todo["name"]
    
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name) VALUES (%s, %s) RETURNING id;", (name))
    todo_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"created": f"{todo_id}", "pod_name": os.getenv("POD_NAME")}), 200

@bp.route("/user", methods=["GET"])
def read_users():
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.close()
    conn.close()

    data = []
    for user in users:
        data.append({"id": user[0], "name": user[1]})

    return jsonify({"items": data, "pod_name": os.getenv("POD_NAME")}), 200

@bp.route("/user/<int:user_id>", methods=["GET"])
def read_user(user_id):
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if user:
        return jsonify({"item": {"id": user[0], "name": user[1]}, "pod_name": os.getenv("POD_NAME")}), 200
    else:
        return jsonify({"message": "User not found", "pod_name": os.getenv("POD_NAME")}), 404
    
@bp.route("/user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    updated_todo = request.json
    name = updated_todo.get("name")

    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("UPDATE users SET name = %s  WHERE id = %s RETURNING id, name", (name, user_id))
    user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if user:
        return jsonify({"item": {"id": user[0], "name": user[1]}, "pod_name": os.getenv("POD_NAME")}), 200
    else:
        return jsonify({"message": "User not found", "pod_name": os.getenv("POD_NAME")}), 404

@bp.route("/user/<int:todo_id>", methods=["DELETE"])
def delete_todo(user_id):
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = %s RETURNING id", (user_id))
    todo = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if todo:
        return jsonify({"message": "User deleted", "pod_name": os.getenv("POD_NAME")}), 200
    else:
        return jsonify({"message": "User not found", "pod_name": os.getenv("POD_NAME")}), 404