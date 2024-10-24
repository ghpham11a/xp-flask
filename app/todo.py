from flask import Blueprint, request, jsonify
from . import db
import os

bp = Blueprint("todo", __name__)

@bp.route("/todo", methods=["POST"])
def create_todo():
    new_todo = request.json
    title = new_todo["title"]
    description = new_todo["description"]
    
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO todos (title, description) VALUES (%s, %s) RETURNING id;", (title, description))
    todo_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"created": f"{todo_id}", "pod_name": os.getenv("POD_NAME")}), 200

@bp.route("/todo", methods=["GET"])
def read_todos():
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM todos")
    todos = cur.fetchall()
    cur.close()
    conn.close()

    data = []
    for todo in todos:
        data.append({"id": todo[0], "title": todo[1], "description": todo[2]})

    return jsonify({"items": data, "pod_name": os.getenv("POD_NAME")}), 200

@bp.route("/todo/<int:todo_id>", methods=["GET"])
def read_todo(todo_id):
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM todos WHERE id = %s", (todo_id,))
    todo = cur.fetchone()
    cur.close()
    conn.close()
    if todo:
        return jsonify({"item": {"id": todo[0], "title": todo[1], "description": todo[2]}, "pod_name": os.getenv("POD_NAME")}), 200
    else:
        return jsonify({"message": "Todo not found", "pod_name": os.getenv("POD_NAME")}), 404
    
@bp.route("/todo/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    updated_todo = request.json
    title = updated_todo.get("title")
    description = updated_todo.get("description")

    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("UPDATE todos SET title = %s, description = %s WHERE id = %s RETURNING id, title, description", (title, description, todo_id))
    todo = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if todo:
        return jsonify({"item": {"id": todo[0], "title": todo[1], "description": todo[2]}, "pod_name": os.getenv("POD_NAME")}), 200
    else:
        return jsonify({"message": "Todo not found", "pod_name": os.getenv("POD_NAME")}), 404

@bp.route("/todo/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM todos WHERE id = %s RETURNING id", (todo_id,))
    todo = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if todo:
        return jsonify({"message": "Todo deleted", "pod_name": os.getenv("POD_NAME")}), 200
    else:
        return jsonify({"message": "Todo not found", "pod_name": os.getenv("POD_NAME")}), 404
    
