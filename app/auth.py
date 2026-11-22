from datetime import datetime,timedelta,timezone
import jwt
import os
from dotenv import load_dotenv
from pwdlib import PasswordHash
load_dotenv()
password_hash = PasswordHash.recommended()

secret_key = os.getenv("JWT_SECRET_KEY")

if not secret_key:
     print("未配置密钥。")

#secret_key = os.environ["JWT_SECRET_KEY"]


def create_access_token(user_id :str) -> str:

    now = datetime.now(timezone.utc)

    expire = now + timedelta(minutes=30)

    payload = {
           "sub":user_id,
           "iat":now,
           "exp":expire
        }

    token = jwt.encode(
           payload,
           secret_key,
           algorithm="HS256"
    )

    return token


def verify_access_token(token :str)->str:

    try:
        decoded_token = jwt.decode(
            token,
            secret_key,
            algorithms=["HS256"]
        )

        user_id = decoded_token.get("sub")

        #检查user_id
        if not isinstance(user_id,str) or not user_id:
             raise ValueError("token缺少有效的用户身份")

        return user_id
        
    except jwt.ExpiredSignatureError:#token过期处理
         raise ValueError("token已过期")

    except jwt.InvalidTokenError:
         raise ValueError("token无效")
      
      

def hash_password(password :str) -> str:
    HS_pass_word =  password_hash.hash(password)#它负责将用户的明文密码转换成适合安全存储的哈希值。
    return HS_pass_word



if __name__  == "__main__":

    hashed = hash_password("23345")
    print("密码哈希结果是:",hashed)
    print("是否与明文相同：",hashed ==2345)

     


            