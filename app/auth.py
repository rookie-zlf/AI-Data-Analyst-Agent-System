from datetime import datetime,timedelta,timezone
import jwt
import os

""" datetime：获取当前时间。
timedelta：计算 Token 有效期。
timezone：指定时区。
jwt：生成和验证 JWT。
os：读取环境变量中的签名密钥。 """

now = datetime.now(timezone.utc)

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
