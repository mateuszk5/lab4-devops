import os
from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        database=os.getenv("DB_NAME", "appdb"),
        user=os.getenv("DB_USER", "appuser"),
        password=os.getenv("DB_PASSWORD", "apppass"),
    )

@app.route("/")
def home():
    return "Witaj w aplikacji DevOps - Lab 4!"

@app.route("/health")
def health():
    return jsonify(status="ok")

@app.route("/db")
def db_check():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        cur.close()
        conn.close()
        return jsonify(database="connected", version=version)
    except Exception as e:
        return jsonify(database="error", message=str(e)), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)