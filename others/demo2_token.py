# -*- coding: utf-8 -*-
from datetime import datetime,timedelta


import jwt
from jwt import PyJWTError


def genrator_jwt():
    """
    生成jwt
    :return:
    """

    expiry=datetime.utcnow()+timedelta(hours=2)
    # 1 构建载荷信息-用户信息+过期时长
    payload_dict={
        "user_id": 66,
        "user_name": "xiaoming",
        "exp": expiry
    }
    # 构建加密秘钥
    secret_key='python41'

    token=jwt.encode(payload=payload_dict,key=secret_key,algorithms='HS256')
    print(token)

    return token

def verify_jwt(token):
    """
    校验jwt
    :param token:
    :return:
    """
    # 1构建秘钥
    secret_key='python41'

    # 2 token校验,返回载荷信息
    try:
        payload=jwt.decode(token,secret_key,algorithms=['HS256'])
    except PyJWTError as e:
        print(e)
        payload=None

        if payload:
            user_id=payload.get('user_id')
            user_name=payload.get('user_name')
            print(user_id,user_name)

import os,base64

if __name__ == '__main__':
    token=genrator_jwt()
    verify_jwt(token)
    # 生成随机秘钥
    print(os.urandom(32))
    # base64编码
    print(base64.b64decode(os.urandom(32).decode()))


