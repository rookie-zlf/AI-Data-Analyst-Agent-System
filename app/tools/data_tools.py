from pathlib import Path
import pandas as pd
from langchain.tools import tool



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

    numeric_df = df.select_dtypes(include = "number")

    if not numeric_df.empty:
        result.append("\n===Numeric Statistics===")
        result.append(numeric_df.describe().to_string())
        return "\n".join(result)
    






    


