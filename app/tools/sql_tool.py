from langchain_core.tools import tool
from app.postgres_store import list_files,count_files


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