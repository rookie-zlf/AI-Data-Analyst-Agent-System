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


def count_files_by_names():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT
                filenames,
                COUNT(*) AS upload_count 
                FROM files
                GROUP BY filename
                ORDER BY upload_count DESC;
                """
            )
            return cursor.fetchall()


def execute_readonly_query(sql:str):#让llm生成查询语言，代码负责验证sql语言的对错
    sql_clean = sql.strip()
    sql_lower = sql_clean.lower()

    if not sql_lower.startswith('select'):
        raise ValueError("只允许执行SELECT查询")

    forbidden_keywords = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "truncate",
        "create",
        "grant",
        "revoke"
    ]

    for keyword in forbidden_keywords:
        if keyword in sql_lower:
            raise ValueError(f"检测到危险sql关键字：{keyword}")

        
    if "limit" not in sql_lower:
        sql_clean = sql_clean.rstrip(";") + "LIMIT 100;"


    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            rows =  cursor.fetchall()
            columns = [
                desc.name for desc in cursor.description
            ]


    result = [
    dict(zip(columns,row)) #zip：一一对应 
    for row in rows
    ]
    return result



def get_database_schema():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
            SELECT 
                table_name,
                column_name,
                data_type 
            FROM information_schema.columns
            WHERE table_schema ='public'
            ORDER BY table_name,ordinal_position;
    """
            )#information_schema.columns,PostgreSQL 用来描述“数据库里有哪些表、每张表有哪些列”的系统信息表。

            rows = cursor.fetchall()

    schema = {}

    for table_name,column_name,data_type in rows:
        if table_name not in schema:
            schema[table_name] = []

        schema[table_name].append(
            {
                'column':column_name,
                'type':data_type
            }
        )

    return schema


#def save_sql_query_log():
 #   session_id:str,


def save_agent_turn(
        turn_id :str,
        session_id:str,
        user_message:str
):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                    INSERT INTO agent_turns(
                    turn_id,
                    session_id,
                    user_message)
                    values(
                    %s,%s,%s)
                """,
                (turn_id,session_id,user_message)
            )




def save_sql_query_log(
        turn_id : str,
        session_id : str,
        sql_text :str,
        status :str,
        error_message : str | None = None
):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO sql_query_logs (
                turn_id,
                session_id,
                sql_text,
                status,
                error_message
                )VALUES(
                %s,%s,%s,%s,%s)
                """,
                (turn_id,session_id,sql_text,status,error_message)
            )
    