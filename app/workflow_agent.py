from typing import TypedDict,NotRequired
from langchain_core.messages import BaseMessage,HumanMessage,AIMessage
from langgraph.graph import START,END,StateGraph



class AgentWorkFlowState(TypedDict):
    messages : list[BaseMessage]
    answer:NotRequired[str]


def build_agent_workflow(agent):
    def run_agent(state:AgentWorkFlowState):
        result = agent.invoke({
            'messages':state['messages']
        })

        return {'answer':result['messages'][-1].content}


    builder = StateGraph(AgentWorkFlowState)
    builder.add_node('run_agent',run_agent)
    builder.add_edge(START,'run_agent')
    builder.add_edge('run_agent',END)


    return builder.compile()


