#把对话信息通过redis持久化存储
import redis
import json

redis_client = redis.Redis(
    host='localhost',
    port = 6379,
    decode_responses=True#解码回答
)


#设置对话过期时间，到期redis自动清理
session_TTL = 60*60*24

def get_session_key(session_id : str) -> str:
    return f"session:{session_id}"



#保存redis信息
def save_session(session_id:str,session_data:dict):
    key = get_session_key(session_id)

    session_json = json.dumps(session_data,ensure_ascii=False)

    #redis以键值对的形式存储
    redis_client.set(
        key,
        session_json,
        ex = session_TTL#到期时间自动清理
    )



#提取redis信息
def get_session(session_id:str)->dict:

    key = session_id

    data = redis_client.get(key)

    if data is None:
        return None

    data_json = json.loads(data)

    return data_json