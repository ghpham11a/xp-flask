import os
import psycopg2
import click
from flask import current_app, g


def get_db():
    if "db" not in g:
        try:
            conn = psycopg2.connect(
                host=os.getenv("POSTGRES_HOST"),
                database=os.getenv("POSTGRES_NAME"),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD")
            )
            g.db = conn
        except psycopg2.DatabaseError as e:
            print(f"Database connection failed: {e}")
            return None
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()