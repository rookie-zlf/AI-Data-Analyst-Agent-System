from langchain_core.messages import HumanMessage
from app.agent import create_data_agent


agent = create_data_agent()


if __name__ == "__main__":
    question = "vip需要满足什么条件？"

    for chunk,metadata in agent.stream(#stream:逐步获得模型生成的内容
        {
            "messages":[HumanMessage(content=question)]
        },
        stream_mode="messages"
    ):
        if (
            metadata.get("langgraph_node") == "model" and 
            isinstance(chunk.content,str)
            and chunk.content
        ):
            print(
                chunk.content,end="",flush = True
            )

    print()