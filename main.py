from app.tools.data_tools import profile_csv,aggregate_csv,filter_csv,top_n_csv
from langchain_deepseek import ChatDeepSeek
from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()

def create_data_agent():
    model= ChatDeepSeek(
        model="deepseek-v4-flash",
        temperature=0
    )

    agent = create_agent(
        model = model,
        tools = [profile_csv,
                  aggregate_csv,
                  filter_csv,top_n_csv],

        #可靠性约束
        system_prompt = """
        你是一个AI数据分析师，你的任务是帮助用户分析数据，提供数据分析建议和可视化方案。
        你可以使用提供的工具来读取和分析CSV文件，并根据分析结果给出有价值的见解。请确保你的回答简明扼要，易于理解。
        规则：
        1.当用户要求查看或分析CSV文件时，应该优先调用可用的数据分析工具。
        2.所有数据结论必须基于工具实际返回的结果。
        3.不得编造工具没有提供的数据、单位、字段含义或统计结果。
        4.如果现有工具不足以完成用户要求，应该明确说明，而不是自行计算或猜测。
        5.样本量较少时，谨慎描述统计规律，避免过度推断。
        7. 如果用户的问题能够直接通过已有分析工具完成，不要为了确认数据结构而重复调用不必要的工具。只有当字段结构不明确时，才优先调用数据概况工具。
        8. 当用户询问“最高、最低的前n条数据等问题时，应使用排序工具，不得自行猜测筛选阈值来代替排序。”
        请用清晰、简洁、有条理的方式回答用户。
        9.如果需要推导其他新指标如：单价、增长率、转化率等，必须先调用工具进行计算，不允许仅凭已有的字段直接推导。
        """
    )
    return agent


def main():
    agent = create_data_agent()
    #记忆对话
    conversation = []
    print('===AI data analyst Agent 已启动=== ')
    print('输入 exit / quit / 退出 可以结束程序')


    while(True):
        user_input = input('\n 你：').strip()
        if user_input.lower() in {'exit','quit','退出'}:
            print('\n agent :再见')
            break
        if not user_input :
            continue

        conversation.append(
            {
                'role':'user',
                'content' :user_input
            }
        )

        try:
            result = agent.invoke(
                {
                    "messages" : conversation,
                }
            )

            for message in result['messages']:
                message.pretty_print()


            #Multi-turn Conversation（多轮对话）。
            conversation = result['messages']
           

            last_message = conversation[-1]
            

            if hasattr(last_message,'content'):
                answer = last_message.content
            else:
                answer = last_message['content']
            print(f'\n Agent:{answer}')

        except Exception as e:
            print(f'发生异常：{e}')

  





if __name__ == "__main__":
    main()



