from pathlib import Path
import shutil
from fastapi import FastAPI,File,UploadFile
from pydantic import BaseModel
from app.agent import create_data_agent


#定义请求模型
class ChatRequest(BaseModel):
    message :str
    session_id :str


agent = create_data_agent()

#临时内存存储
chat_sessions = {}


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


current_file_path : str | None = None


@app.post("/upload")

#需要用户上传一个csv文件
def up_load_csv(
    file : UploadFile = File(...)
):
    global current_file_path 

    #防止文件名里面携带路径
    filename = Path(file.filename).name

    if not filename.lower().endswith(".csv"):
        return {
            "success":False,
            "mesage":"目前只支持CSV文件"
        }
    
    save_path = UPLOAD_DIR / filename

    with save_path.open('wb') as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    current_file_path = str(save_path)


    return {
        "success":True,
        "filename":filename,
        "file_path":str(save_path)
    }


@app.post("/chat")
def chat(requset : ChatRequest):
    if current_file_path is None:
        return {
            "success":False,
            "message":"请先上传csv文件。"
        }


    session_id = requset.session_id


    #新会话，创建历史记录
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []


    user_message = (
        f'当前需要分析的csv文件路径是{current_file_path}\n'
        f'用户问题:{requset.message}'
    )

    #加入历史
    
    chat_sessions[session_id].append(
        {
            'role':'user',
            'content':user_message
        }
    )


    result = agent.invoke(
        {
            "messages":chat_sessions[session_id]     
        }
    )

    last_message = result['messages'][-1]

    if hasattr(last_message,'content'):
        answer = last_message.content
    else:
        answer = last_message['content']


    chat_sessions[session_id].append(
        {
            'role' : 'assistant',
            'content': answer
        }
    )


    return {
        'success':True,
        'session_id':session_id,
        'answer':answer
    }