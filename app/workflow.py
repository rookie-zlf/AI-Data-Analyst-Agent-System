from typing import TypedDict,NotRequired
from langgraph.graph import StateGraph,START,END
from app.tools.rag_tools import search_knowlege_base




class WorkflowState(TypedDict):
    question:str
    clean_question :NotRequired[str]
    result: NotRequired[str]


def prepare_question(state:WorkflowState):
    return {
        "clean_question":state['question'].strip()
    }

def route_question(state:WorkflowState) -> str:
    question = state['clean_question'].lower()

    if 'vip' in question or '定义' in question:
        return "rag"

    if "上传" in question:
        return "sql"

    return "csv" 

def rag_node(state:WorkflowState):
    question = state["clean_question"]
    result = search_knowlege_base.invoke(
        {"query":question}
    )
    return {'result':result}


def sql_node(state:WorkflowState):
    return {"result":"选择了 PostgreSQL 查询"}

def csv_node(state:WorkflowState):
    return {'result':'选择了 CSV 数据分析'}

builder = StateGraph(WorkflowState)

builder.add_node("prepare_question",prepare_question)

builder.add_edge(START,"prepare_question")
builder.add_node('rag_node',rag_node)
builder.add_node('sql_node',sql_node)
builder.add_node('csv_node',csv_node)

builder.add_conditional_edges(
    "prepare_question",
    route_question,
    {
        'rag':'rag_node',
        'sql':'sql_node',
        'csv':'csv_node'
    }
)


builder.add_edge("rag_node",END)
builder.add_edge("sql_node",END)
builder.add_edge('csv_node',END)


workflow = builder.compile()


if __name__ == "__main__":

 questions = [
    "VIP 客户标准是什么？",
    "sales.csv 上传过几次？",
    "MacBook 的总销售额是多少？"
 ]

for question in questions:
    result = workflow.invoke({
        "question":question
    })
    print(question,'->',result['result'])

