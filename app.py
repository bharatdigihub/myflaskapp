from flask import Flask
import os
import time
import psycopg2
from psycopg2 import OperationalError

app = Flask(__name__)


def get_db_connection(retries=5, delay=2):
    """Attempt to connect to Postgres using env vars with retries.

    Returns a psycopg2 connection or raises the last exception.
    """
    host = os.environ.get("DB_HOST")
    port = int(os.environ.get("DB_PORT", "5432"))
    user = os.environ.get("DB_USER")
    password = os.environ.get("DB_PASSWORD")
    dbname = os.environ.get("DB_NAME")

    # Validate required environment variables
    missing_vars = []
    if not host:
        missing_vars.append("DB_HOST")
    if not user:
        missing_vars.append("DB_USER")
    if not password:
        missing_vars.append("DB_PASSWORD")
    if not dbname:
        missing_vars.append("DB_NAME")
    
    if missing_vars:
        raise ValueError(f"Missing required database environment variables: {', '.join(missing_vars)}")

    last_exc = None
    for attempt in range(1, retries + 1):
        try:
            # Configure connection with SSL required (needed for Render.com's Postgres)
            conn = psycopg2.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                dbname=dbname,
                sslmode='require'  # Render.com requires SSL
            )
            return conn
        except OperationalError as e:
            last_exc = e
            app.logger.warning(f"Postgres connection attempt {attempt} failed: {e}")
            time.sleep(delay)

    # All retries failed
    raise last_exc


@app.route('/')
def hello():
    try:
        db_connection = get_db_connection()
    except Exception as e:
        return f"Database connection failed: {e}", 500

    cursor = db_connection.cursor()
    cursor.execute('SELECT current_database();')
    db_name = cursor.fetchone()
    cursor.close()
    db_connection.close()
    return f"Connected to Postgres database: {db_name[0]}"


if __name__ == '__main__':
    # Use PORT environment variable if available (for Render.com), fallback to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
