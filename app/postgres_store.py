import os
import psycopg
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    conn = psycopg.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=int(os.getenv("POSTGRES_PORT")),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    return conn



def create_file_record(
        session_id : str,
        filename : str,
        file_path : str
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """INSERT INTO files (session_id,filename,file_path) VALUES (%s,%s,%s)"""
        ,
        (session_id,filename,file_path,)
    )
    conn.commit() # 提交事务,正式确认修改

    cursor.close()
    conn.close()