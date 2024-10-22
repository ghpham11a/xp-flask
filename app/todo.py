from flask import Blueprint
from flask import Flask

bp = Blueprint("todo", __name__)

@bp.route('/todo', methods=["GET"])
def read_todos():
    return 'index'

@bp.route('/todo/<int:todo_id>', methods=["GET"])
def read_todo(todo_id):
    return f"reading todo {todo_id}"