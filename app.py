from flask import Flask
import psycopg2
import os

app = Flask(__name__)

@app.route('/')
def index():
    try:
        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST"),
            database=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            port=os.environ.get("DB_PORT")
        )
        cur = conn.cursor()
        cur.execute("SELECT current_database();")
        db_name = cur.fetchone()
        cur.close()
        conn.close()
        return f"✅ Connected to PostgreSQL database: {db_name[0]}"
    except Exception as e:
        return f"❌ Database connection failed: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
