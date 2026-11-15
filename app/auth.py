from datetime import datetime,timedelta,timezone
import jwt
import os

""" datetime：获取当前时间。
timedelta：计算 Token 有效期。
timezone：指定时区。
jwt：生成和验证 JWT。
os：读取环境变量中的签名密钥。 """

""" now = datetime.now(timezone.utc)

expire = now + timedelta(minutes=30)

print('签发时间:',now)
print("到期时间",expire)

payload = {
    "sub":"user_001",
    "iat":now,
    "exp":expire
}

secret_key = os.environ["JWT_SECRET_KEY"]


token = jwt.encode(
    payload,           #要写入 JWT 的身份和时间信息
    secret_key,        #签名密钥
    algorithm="HS256"  #指定 HMAC-SHA256 签名算法
)

print("jwt生成成功：",isinstance(token,str))


decoded_payload = jwt.decode(
    token,
    secret_key,
    algorithms=["HS256"]#允许一个算法队列
)


print("解码结果",decoded_payload)



expired_payload = {
    "sub":"user_001",
    "iat":now - timedelta(hours=1),
    "exp":now - timedelta(minutes=1)
}

expired_token = jwt.encode(
    expired_payload,
    secret_key,
    algorithm="HS256"
)

try:
        decoded_expired_payload = jwt.decode(
            expired_token,
            secret_key,
            algorithms=["HS256"]
        )

except jwt.ExpiredSignatureError:
        print("Token已过期，请重新登录") """

secret_key = os.environ["JWT_SECRET_KEY"]

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
      
      
      
if __name__  == "__main__":


       
       token_a = create_access_token("user_001")
       token_b = create_access_token("user_002")

       print("tokenA:",verify_access_token(token_a))
       print("tokenB:",verify_access_token(token_b))

       try:
            verify_access_token("无效token")
       except ValueError as e:
            print("验证失败",e)