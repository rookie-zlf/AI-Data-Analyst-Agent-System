from langchain_core.tools import tool
from app.postgres_store import list_files,count_files,execute_readonly_query,get_database_schema,save_sql_query_log,count_files_by_names
import logging
from app.trace_context import (current_turn_id,current_session_id)


logger = logging.getLogger(__name__)


@tool
def list_uploaded_files(limit: int = 10):
    """查询最近上传的文件记录。
        当用户询问最近上传了哪些文件、上传历史、文件列表时使用。
    """
    rows = list_files(limit)
    return rows


@tool
def count_upload_files():
    """统计表中所有的数据个数，结果返回的是一个数字，代表这个表里一共有几条数据。
        当用户询问“我一共上传了多少文件”, “一共有多少条记录”等问题时使用。"""
    total_numbers = count_files()
    return total_numbers


@tool
def get_file_upload_statistics():
    """统计每个文件名分别有多少条上传记录
    当用户询问某个文件上传了几次、哪个文件上传次数最多、各个文件上传次数分布等问题时使用。"""
    sql = """
            SELECT 
                    filename,
                    COUNT(*) AS upload_count
            FROM 
                    files
            GROUP BY 
                    filename
            ORDER BY
                    upload_count 
            DESC;
            """
    return execute_and_trace_sql(
        sql= sql,
        source = "fixed_tool",
        tool_name= 'get_file_upload_statistics'
    )

@tool
def execute_sql_query(sql:str):
    """执行 PostgreSQL 只读 SELECT 查询。

    当用户的问题需要根据数据库内容进行动态查询，
    且现有固定 SQL 工具无法直接回答时使用。

    只能执行 SELECT 查询，不允许修改数据库。"""
    session_id = current_session_id.get()
    turn_id = current_turn_id.get()

    if session_id is None or turn_id is None:
        raise RuntimeError('缺少当前 SQL Trace 上下文')

    try:
        result = execute_readonly_query(sql)
    except Exception as e:
        #SQL sql本身执行失败
        try:
            save_sql_query_log(
                turn_id = turn_id,
                session_id= session_id,
                sql_text=sql,
                status="failed",
                error_message=str(e)
            )
        except Exception:
            logger.exception(
                "保存失败SQL日志时发生异常，turn_id = %s",
                turn_id
            )
        raise
    #SQL执行成功
    try:
        save_sql_query_log(
            turn_id = turn_id,
            session_id=session_id,
            sql_text = sql,
            status="success"
        )
    except Exception:
        logger.exception(
            "SQL执行成功但是SQL保存失败，turn_id = %s",
            turn_id
        )
    
    return {
        'sql':sql,
        'result':result
    }
    


@tool
def get_sql_schema():
    """获得PostgreSQL数据库中表的结构信息。
        当需要生成动态SQL、但不确定数据库有哪些表或字段时使用。"""

    return get_database_schema()




def execute_and_trace_sql(
        sql:str,
        source:str,
        tool_name:str
):
    session_id = current_session_id.get()
    turn_id = current_turn_id.get()

    if session_id is None or turn_id is None:
        raise RuntimeError("缺少SQL Trace 上下文。")

    try:
        result = execute_readonly_query(sql)
    except Exception as e:
        try:
            save_sql_query_log(
                turn_id = turn_id,
                session_id=session_id,
                sql_text = sql,
                status='failed',
                source=source,
                tool_name=tool_name,
                error_message=str(e)
            
            )
        except Exception:
            logger.exception(
                '保存失败SQL日志发生异常，turn_id',
                turn_id
            )
        raise
    try:
        save_sql_query_log(
            turn_id = turn_id,
            session_id=session_id,
            sql_text = sql,
            status='success',
            source=source,
            tool_name=tool_name,                 
        )
    except Exception:
        logger.exception(
            'sql执行成功，但是日志保存失败,turn_id = %s',
            turn_id
        )
    return result



    

    
    
