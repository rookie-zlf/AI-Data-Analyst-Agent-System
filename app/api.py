from pathlib import Path
import shutil
from fastapi import FastAPI,File,UploadFile
from pydantic import BaseModel
from app.agent import create_data_agent
from uuid import uuid4
#langchain官方的消息对象，不用自己手动维护dict消息1队列
from langchain_core.messages import HumanMessage,AIMessage


#定义请求模型
class ChatRequest(BaseModel):
    message :str
    session_id :str


agent = create_data_agent()

sessions = {}

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
    save_path = UPLOAD_DIR / f'{session_id}_{filename}'

    with save_path.open('wb') as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    sessions[session_id] = {
        'file_path':save_path,
        'messages':[]
    }

    return {
        "success":True,
        "session_id":session_id,
        "filename":filename,
        "file_path":str(save_path)
    }


@app.post("/chat")
def chat(requset : ChatRequest):

    session_id = requset.session_id

    if session_id  not in sessions:
        return {
            "success":False,
            "message":"session不存在，请先上传csv文件。"
        }


    session = sessions[session_id]

    file_path = session['file_path']
    messages = session['messages']

    user_message = (
        f"当前需要分析的的CSV文件路径是：{file_path}\n"
        f"用户的问题:{requset.message}"
    )

    messages.append(
        HumanMessage(content=user_message)
    )

    #包含hunman，toolcall的所有消息,'把干净历史喂给agent'
    result = agent.invoke(
        {
            'messages' : messages
        }
    )

    last_message = result['messages'][-1]

    answer = last_message.content

    messages.append(
        AIMessage(content=answer)
    )

    sessions[session_id]["messages"] = messages

    return {
        'success':True,
        'session_id':session_id,
        'answer':answer
    }




