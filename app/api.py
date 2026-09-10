from pathlib import Path
import shutil
from fastapi import FastAPI,File,UploadFile
from pydantic import BaseModel
from app.agent import create_data_agent
from uuid import uuid4
from app.postgres_store import create_file_record,delete_file_record

#langchain官方的消息对象，不用自己手动维护dict消息1队列
from langchain_core.messages import HumanMessage,AIMessage
from app.session_store import save_session,get_session,get_session_ttl,delete_session


#定义请求模型
class ChatRequest(BaseModel):
    message :str
    session_id :str


agent = create_data_agent()

#创建后端应用
app = FastAPI(
    title = "AI Data Analyst Agent System"
              )


UPLOAD_DIR = Path("data/uploads")

UPLOAD_DIR.mkdir(parents=True,exist_ok=True)


@app.get("/")
def root():
    return {
        "message":"AI Data Analyst Agent System is running"
    }


@app.post("/upload")

#需要用户上传一个csv文件
def up_load_csv(
    file : UploadFile = File(...)
):
  
    filename = Path(file.filename).name
    if not filename.lower().endswith('.csv'):
        return {
            'success':False,
            'message':'目前只支持CSV文件'
        }

    session_id = str(uuid4())
    #是一个path对象，保存文件的路径，可以通过调用对象方法操作文件
    save_path = UPLOAD_DIR / f'{session_id}_{filename}'
    try:
        with save_path.open('wb') as buffer:
            shutil.copyfileobj(
                 file.file,
                 buffer
                )

        session_data = {
            'file_path':str(save_path),
            'messages':[]
         }


        save_session(session_id,session_data)

        create_file_record(session_id,filename,str(save_path))

        return {
                "success":True,
                "session_id":session_id,
                "filename":filename,
                "file_path":str(save_path)
          }
    except Exception as e:
        delete_session(session_id)
        if save_path.exists():
            save_path.unlink()#删除这个文件
        delete_file_record(session_id)
        

        return {
            "success":False,
            "message":f'上传文件失败：{str(e)}'
        }        
        

@app.post("/chat")## 每次 /chat 请求最终只保存一条用户消息和一条最终 AI 回复到 Redis
def chat(request : ChatRequest):

    session_id = request.session_id
    #查看对话剩余时间
    life_remain_time = get_session_ttl(session_id)

    sessions_data = get_session(session_id)

    if sessions_data is None:
        return f"{request.session_id}不存在。"

    file_path = sessions_data['file_path']
    messages = sessions_data['messages']

    user_message = (
        f"当前需要分析的的CSV文件路径是：{file_path}\n"
        f"用户的问题:{request.message}"
    )

    messages.append(
        {
            'role':'user',
            'content':user_message
        }
    )

    #格式翻译，将json格式翻译成langchain的格式

    langchain_messages = []

    #is比较是否为同一个对象，==比较值是否相等
    for message  in sessions_data['messages']:
        if message['role'] == 'user':
            langchain_messages.append(HumanMessage(content=message['content']))
        elif message['role'] == 'assistant':
            langchain_messages.append(AIMessage(content = message['content']))



    #包含hunman，toolcall的所有消息,'把干净历史喂给agent'
    result = agent.invoke(
        {
            'messages' : langchain_messages
        }
    )

    last_message = result['messages'][-1]

    answer = last_message.content

    messages.append(
        {
            'role':'assistant',
            'content':answer
        }
    )

    sessions_data['messages'] = messages

    save_session(request.session_id,sessions_data)

    return {
        'success':True,
        'session_id':session_id,
        'answer':answer,
        'remain_time':life_remain_time
    }




