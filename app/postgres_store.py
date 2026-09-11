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
   
    #正常离开 with→ commit，异常离开 with→ rollback，由psycopg管理这个过程
   with get_connection() as conn:
        #自动保护写入数据，替代cursor.close()防止数据泄露
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



def list_files(limit : int =10):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT id,session_id,filename,created_at
                FROM files
                ORDER BY id
                LIMIT %s"""
                ,
                (limit,)
            ) 
            return cursor.fetchall()


def count_files():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT COUNT(*) FROM files;
                """#统计表内所有信息
            )
            row = cursor.fetchone()#返回一个元组
            return row[0]