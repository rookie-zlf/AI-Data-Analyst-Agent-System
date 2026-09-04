import os
import psycopg
from dotenv import load_dotenv
from postgres_store import create_file_record

load_dotenv()

conn = psycopg.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=int(os.getenv("POSTGRES_PORT")),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
)

create_file_record("12345678-1234-1234-1234-123456789abc", "demo.csv","data/uploads/demo.csv")


cursor = conn.cursor()

cursor.execute("""
SELECT * FROM files ORDER BY id DESC LIMIT 3;""")

rows = cursor.fetchall()

print(rows)




