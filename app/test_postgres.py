import os
import psycopg
from dotenv import load_dotenv
from postgres_store import (create_file_record,list_files,
                            execute_readonly_query,get_database_schema,
                            save_agent_turn,save_sql_query_log
)

from uuid import uuid4

load_dotenv()

turn_id = str(uuid4())

session_id = str(uuid4())

save_agent_turn(
    turn_id,session_id,'ales.csv 上传过几次？'
)

save_sql_query_log(
    turn_id,session_id,"SELECT COUNT(*) FROM files WHERE filename = 'sales.csv'","success"
)
