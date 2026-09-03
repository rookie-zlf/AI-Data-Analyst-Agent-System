import os
import psycopg
from dotenv import load_dotenv

load_dotenv()


conn = psycopg.connect(
    host = os.getenv("POSTGRES_HOST"),
    port = int (os.getenv("POSTGRES_PORT")),
    dbname = os.getenv("POSTGRES_DB"),
    user = os.getenv("POSTGRES_USER"),
    password  = os.getenv("POSTGRES_PASSWORD")
)


print("Post 连接成功")

cursor = conn.cursor()

#执行查询
cursor.execute(
    """SELECT id,filename,created_at 
        FROM files;
        """
)

cursor.execute(
    """SELECT id,filename,created_at 
        FROM files where id=1;
        """
)
#拿出所有查询结果,返回一个列表
rows = cursor.fetchall()

row = rows[0]

print(row)


cursor.close()
conn.close()

