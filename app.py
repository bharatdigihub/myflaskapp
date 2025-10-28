from flask import Flask
import mysql.connector
import os

app = Flask(__name__)

@app.route('/')
def hello():
    db_connection = mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
    )
    cursor = db_connection.cursor()
    cursor.execute("SELECT DATABASE();")
    db_name = cursor.fetchone()
    cursor.close()
    db_connection.close()
    return f"Connected to MySQL database: {db_name[0]}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
