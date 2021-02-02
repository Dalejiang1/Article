from flask import current_app, g
from flask_restful import Resource
import random
from app import redis_client, db
from models.user import User
from utils.constants import SMS_CODE_EXPIRE
from flask_restful.reqparse import RequestParser
from datetime import datetime, timedelta
from utils.jwt_util import generate_jwt
from flask_restful.inputs import regex
from sqlalchemy.orm import load_only
class SMSCodeResource(Resource):
    """发送短信验证码视图类"""
    def get(self,mobile):
        # 1生成随机6位数短信验证码
        sms_code="06%d"%(random.randint(0,999999))
        # 保存验证码（code） app:code:13112341234 123456
        sms_code="123456"

        # 2.存储到redis数据库 设置过期时长【5分钟】
        key="app:code:{}".format(mobile)

        redis_client.set(key,sms_code,ex=SMS_CODE_EXPIRE)

        # 3发送短信验证码
        # TODO 调用第三方平台发送短信验证码
        # print('短信验证码: "mobile": {}, "code": {}'.format(mobile, sms_code))
        # 4返回响应
        return {"smscode":sms_code,"mobile":mobile}

        # return {"foo":"get"}


class LoginRegisterResource(Resource):
    """登录注册接口"""
    """
        登录、注册接口思路：
        # 1.获取参数
        # 1.1 mobile 手机号码
        # 1.2 smscode 用户填写的短信验证码
        # 2.参数校验--RequestParser参数提取和参数校验
        # 3.业务逻辑
        # 3.1 根据手机号码获取redis数据库中真实的短信验证码
        # 3.1 删除redis数据库中的真实短信验证码-防止一个短信验证多次验证
        # 3.2 对比用户填写的短信验证和真实短信验证码是否一致
        # 3.3 短信验证码通过
        # 3.4 根据手机号码作为查询条件，查询用户对象是否存在
        # 3.5 用户不存在--注册
        # 3.6 新建用户对象，添加到会话层
        # 3.5 用户对象存在--登录，修改最后一次登录时间
        # 3.7 将上述新增修改操作提交到数据库
        # 3.8 生成2小时有效的登录token和14天有效的刷新token
        # 4.返回值处理
        """
    def get_token(self,user_id):
        """
                生成2小时有效的登录token和14天有效的刷新token
                :param user_id: 当前用户id
                :return:
                """
        # 1生成2小时有效登录token
        login_payload={
            "user_id":user_id,
            "is_refrech":False
        }
        # 过期时长
        expiry_2h=datetime.utcnow() + timedelta(hours=current_app.config["JWT_EXPIRE_2H"])
        expiry_14d=datetime.utcnow() + timedelta(days=current_app.config["JWT_EXPIRE_14D"])

        # 获取秘钥
        secret_key=current_app.config['JWT_SECRET']

        # 生成登录token
        login_token=generate_jwt(payload=login_payload,expiry=expiry_2h,secret=secret_key)

        # 生成14天有效的刷新token
        refresh_payload={
            "user_id": user_id,
            "is_refresh": True
        }
        # 生成刷新token
        refresh_token=generate_jwt(payload=refresh_payload,expiry=expiry_14d,secret=secret_key)

        return login_token,refresh_token

    def post(self):
    # 1.获取参数 -- post请求体以json格式传递参数
    # 1.1 mobile 手机号码
    # 1.2 code 用户填写的短信验证码
    # 2.参数校验--RequestParser参数提取和参数校验
    # 构建解析对象
        parser=RequestParser()

        parser.add_argument("mobile", required=True, location="json", type=regex(r'^1[3-9]\d{9}$'))
        parser.add_argument("code", required=True, location="json", type=regex(r'\d{6}'))

        param_ret=parser.parse_args()
        mobile=param_ret['mobile']
        sms_code=param_ret['sms_code']
    # 3业务逻辑处理
        key="app:code:{}".format(mobile)
        real_smscode=redis_client.get(key)
        redis_client.delete(key)

        if real_smscode is None:
            return {"message":"短信验证码为空"}
        if sms_code != real_smscode:
            return {"message":"短信验证码错误"}

    # 3.3 短信验证码通过
    # 3.4 根据手机号码作为查询条件，查询用户对象是否存在
    # select * from xxxx where xx
    # 优化查询：options(load_only(User.id))
        user=User.query.options(load_only(User.id)).filter(User.mobile==mobile).first()
        if user is None:
            user=User(mobile=mobile,name=mobile,last_login=datetime.now())
            db.session.add(user)
        else:
            user.last_login=datetime.now()

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"message":f"数据库提交异常{e}"},507
        # 3.8 生成2小时有效的登录token和14天有效的刷新token
        login_token,refresh_token=self.get_token(user_id=user.id)

        # 4返回值处理
        return {"login_token": login_token, "refresh_token": refresh_token}
    def put(self):
        """刷新token的后端接口"""
        user_id = g.user_id
        is_refresh=g.is_refresh

        # 刷新token
        if user_id and is_refresh is True:
            login_token,_=self.get_token(user_id)
            return {"new_token":login_token}
        else:
            # 刷新token失效
            return {"message":"refresh刷新token失效"}










