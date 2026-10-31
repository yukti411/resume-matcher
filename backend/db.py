import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_conn():
    return mysql.connector.connect(
        host="localhost", user="root",
        password=os.getenv("DB_PASSWORD"), database="resume_matcher"
    )

def save(result):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO analyses (score, matched, missing) VALUES (%s, %s, %s)",
        (result["score"], ", ".join(result["matched"]), ", ".join(result["missing"])),
    )
    conn.commit()
    conn.close()

def history():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM analyses ORDER BY id DESC LIMIT 20")
    rows = cur.fetchall()
    conn.close()
    return rows