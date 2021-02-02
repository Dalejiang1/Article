import jwt
from flask import current_app


def generate_jwt(payload, expiry, secret=None):
    """
    生成jwt
    :param payload: dict 载荷
    :param expiry: datetime 有效期
    :param secret: 密钥
    :return: jwt
    """
    # 过期时长固定的key: exp
    _payload = {'exp': expiry}
    # 字典更新方法，添加新的键值对
    _payload.update(payload)

    """
    _payload =  {
        "user_id": 66,
        "user_name": "xiaoming",
        "exp": expiry

    }
    """

    # 没有传入秘钥
    if not secret:
        # 读取配置文件中的秘钥
        # 使用current_app代替app对象
        secret = current_app.config['JWT_SECRET']

    # 生成token
    token = jwt.encode(_payload, secret, algorithm='HS256')

    # 返回字符串类型的token
    return token.decode()


def verify_jwt(token, secret=None):
    """
    检验jwt
    :param token: jwt
    :param secret: 密钥
    :return: dict: payload
    """
    if not secret:
        secret = current_app.config['JWT_SECRET']

    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
    except jwt.PyJWTError:
        payload = None

    # payload 有可能为空
    return payload

