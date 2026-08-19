from app.tools.data_tools import profile_csv
from langchain_deepseek import ChatDeepSeek
from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()

def main():
    model= ChatDeepSeek(
        model="deepseek-v4-flash",
        temperature=0.2
    )
    agent = create_agent(
        model = model,
        tools = [profile_csv],

        #可靠性约束
        system_prompt = """
        你是一个AI数据分析师，你的任务是帮助用户分析数据，提供数据分析建议和可视化方案。
        你可以使用提供的工具来读取和分析CSV文件，并根据分析结果给出有价值的见解。请确保你的回答简明扼要，易于理解。
        规则：
        1.当用户要求查看或分析CSV文件时，应该优先调用可用的数据分析工具。
        2.所有数据结论必须基于工具实际返回的结果。
        3.不得编造工具没有提供的数据、单位、字段含义或统计结果。
        4.如果现有工具不足以完成用户要求，应该明确说明，而不是自行计算或猜测。
        5.样本量较少时，赢谨慎描述统计规律，避免过度推断。

        请用清晰、简洁、有条理的方式回答用户。
        """
    )

    """ response = model.invoke(
        "请问你能干什么"
    )
    print(response.content) """
    
    result = agent.invoke(
        {
            "messages":[
                {
                    'role':'user',
                    'content':'请帮我分析一下这个csv文件，文件地址是：/Users/sunflower_zlf/AI_Data_Analyst_Agent_System/data/sales.csv'
                    #'content':'你好'
                }
            ]
        }
    )
    print(result['messages'][-1].content)

    """ for message in result['messages']:
        message.pretty_print() """
    


if __name__ == "__main__":
    main()
