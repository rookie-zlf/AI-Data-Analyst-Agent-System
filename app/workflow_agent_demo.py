from typing import TypedDict,NotRequired
from langgraph.graph import StateGraph,START,END
from langchain_core.messages import HumanMessage

from app.agent import create_data_agent

agent = create_data_agent()

class AgentWorkflowState(TypedDict):
    question:str
    answer:NotRequired[str]



def run_agent(state:AgentWorkflowState):

    #与大模型交互转换成human语言
    result = agent.invoke(
        {'messages':HumanMessage(content=state['question'])}
    )

    answer = result['messages'][-1].content

    return {
        'answer':answer
    }


builder = StateGraph(AgentWorkflowState)

builder.add_node("run_agent",run_agent)

builder.add_edge(START,'run_agent')

builder.add_edge('run_agent',END)

#整合图传给workflow
workflow = builder.compile()

if __name__ == "__main__":

    result =  workflow.invoke({
        "question":  "VIP 客户需要满足什么条件？"    
    })

    print(result['question'],"\n",result['answer'])


