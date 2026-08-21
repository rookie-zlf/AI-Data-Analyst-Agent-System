from pathlib import Path
import pandas as pd
from langchain.tools import tool
from typing import Literal



@tool
def profile_csv(file_path: str) -> str:
    '''read a csv file and return its basic adta profile'''

    path = Path(file_path)

    if not path.exists():
        return f"file {file_path} does not exist"

    try:
        df = pd.read_csv(path)
    except Exception as e:
        return f"Failed to read csv: {e}"

    result = []
    result.append("===dataset overview===")
    result.append(f"Rows:{df.shape[0]}")
    result.append(f"Columns:{df.shape[1]}")
    result.append("\n===columns===")
    result.append(",".join(df.columns))
    result.append("\n===data types===")
    result.append(df.dtypes.to_string())

    result.append("\n===missing values===")
    result.append(df.isnull().sum().to_string())
    result.append("\n===Duplicate rows===")
    result.append(str(df.duplicated().sum()))

    numeric_df = df.select_dtypes(include = "number")

    if not numeric_df.empty:
        result.append("\n===Numeric Statistics===")
        result.append(numeric_df.describe().to_string())
        return "\n".join(result)
    




@tool
def aggregate_csv(
    file_path : str,
    metric: str,
    operation: Literal['sum','mean','max','min','count'] = 'sum',
     group_by: str | None = None,
     filters: dict[str,str] | None = None
)->str:

    """对csv数据进行分组聚合分析。
    当用户要求按某个字段分组，并计算总和、平均值、最大值、最小值或数量时使用这个工具。
    Args:
        file_path:csv文件路径
        group_by：用于分组的字段名
        metric：需要统计的字段名
        operation：聚合方式，可选 sum、mean、max、min、count
        filters:可筛选条件，例如：{"product":"MacBook","region":"East"}
        """
    path = Path(file_path)
    if not path.exists():
        return f"文件不存在：{file_path}"

    try:
        df = pd.read_csv(path)
    except Exception as e:
        return f"读取文件失败：{e}"
        
    #条件筛选，for循环多次过滤pd文件
    if filters:
        for column,value in filters.items():
            if column not in df.columns:
                return f'筛选字段不存在：{column}'

            df = df[
                df[column].astype(str).str.lower() == str(value).lower()
            ]

    if df.empty:
        return f'筛选后没有数据。'

    #检查统计字段
    if metric not in df.columns:
        return f"统计字段不存在:{metric}"

    try:
        if group_by:
            if group_by not in df.columns:
                return f'分组字段不存在{group_by}'
            
            result = (
                df.groupby(group_by)[metric]
                .agg(operation)
                .sort_values(ascending=False)
            )
            return result.to_string()

        #不分组，直接计算
        result = df[metric].agg(operation)
        return f'{operation}({metric}) = {result}'
    

    except Exception as e:
        return f"聚合分析失败：{e}"



    
@tool
def filter_csv(
    file_path : str,
    column : str,
    operator : str,
    value: str,
) -> str:
    """根据条件筛选CSV数据。
    当用户要求查找满足某些条件的数据记录时使用。
    Args:
        file_path: csv路径
        column:筛选字段，例如 sales、product、region
        operator:比较方式：>,<,>=,<=,==
        value:筛选目标值"""

    path = Path(file_path)
    if not path.exists():
        return f'目标csv文件不存在:{Path}'

    try:
        df = pd.read_csv(path)

    except Exception as e:
        print(f'读取失败：{e}')

    if column not in df.columns:
        return f'字段不存在:{column}'

    try:
        #'==' 需要去除，因为‘==’不仅可以用来匹配数字，也可以用来匹配字符串，当字符串匹配时，发现不能转换成数字自动删掉字符串变成NaN
            if operator in {'>','<','>=','<='}:
                df[column] = pd.to_numeric(
                    df[column],
                    errors='coerce'
                )
                value = float(value)

            if operator == '>':
                result = df[df[column]>value]
            elif operator == '<':
                result = df[df[column]<value]
            elif operator == '>=':
                result = df[df[column] >= value]
            elif operator == '<=':
                result = df[df[column] <= value]
            elif operator == '==':
                result = df[
                    df[column].astype(str).str.lower()==str(value).lower()
                ]
            else:
                return f'不支持的操作符:{operator}'

    except Exception as e:
            return f'筛选失败:{e}'

    if result.empty:
        return "没有找到符合条件的数据"

    return result.to_string(index = False)
    

            



    