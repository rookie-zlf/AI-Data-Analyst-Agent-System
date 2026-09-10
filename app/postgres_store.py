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
   with get_connection() as conn:#自动保护写入数据，替代cursor.close()防止数据泄露
        with conn.cursor() as cursor:

            cursor.execute(
                """INSERT INTO files (session_id,filename,file_path) VALUES (%s,%s,%s)"""
                ,
                (session_id,filename,file_path,)
            )
    

    




def delete_file_record(session_id :str):

   with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM files WHERE session_id = %s",
                (session_id,)
            )
    