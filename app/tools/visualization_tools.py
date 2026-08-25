from pathlib import Path
import pandas as pd
import matplotlib
# 强制开启“后台默默画图”模式，不弹窗
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from langchain.tools import tool

@tool
def plot_bar_chart(
    file_path :str,
    category_column : str,
    value_column : str,
    out_put_path  = '/Users/sunflower_zlf/AI_Data_Analyst_Agent_System/app/output/bar_chart.png'
)  -> str:
    '''根据csv数据生成柱状图。
    适用于：
    -产品销售额对比
    -区域销售额对比
    -分类统计可视化
    Args:
        file_path:csv文件路径,
        category_column:分类字段，例如：product、region
        value_column:数值字段，例如：sales、quantity
        output_path:图片保存路径'''

    path = Path(file_path)

    if not path.exists():
        return f'文件不存在：{file_path}'

    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        return f'文件读取失败：{e}'

    if category_column not in df.columns:
        return f'不存在字段：{category_column}'
    if value_column not in df.columns:
        return f"不存在字段：{value_column}"

    data =( 
        df.groupby(category_column)[value_column]
        .sum()
        .sort_values(ascending=False)
        )

    plt.figure(figsize=(8,5))

    data.plot(kind = 'bar')

    plt.title(
        f'{category_column} by {value_column}'
    )

    plt.xlabel(
        category_column
    )
    plt.ylabel(
        value_column
    )

    plt.tight_layout()

    output = Path(out_put_path)

    output.parent.mkdir(
        exist_ok= True
    )
    plt.savefig(output)
    plt.close()

    return f'图片生成成功：{output}'


