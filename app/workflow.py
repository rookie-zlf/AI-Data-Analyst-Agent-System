from typing import TypedDict,NotRequired
from langgraph.graph import StateGraph,START,END

class WorkflowState(TypedDict):
    question:str
    clean_question :NotRequired[str]



