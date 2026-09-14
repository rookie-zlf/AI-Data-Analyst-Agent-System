import os
import psycopg
from dotenv import load_dotenv
from postgres_store import create_file_record,list_files,execute_readonly_query,get_database_schema

load_dotenv()

conn = psycopg.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=int(os.getenv("POSTGRES_PORT")),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
)

#cows = list_files()
#cows = execute_readonly_query("SELECT id,filename FROM files LIMIT 5")

cows = get_database_schema()
print(cows)

