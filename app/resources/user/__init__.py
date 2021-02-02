# 蓝图初始化文件
from flask import Blueprint
from flask_restful import Api

# 1.创建蓝图对象管理用户模块
user_bp = Blueprint("user", __name__, url_prefix='/app')

# 2.将蓝图对象包装成具备有restful风格的api对象
user_api = Api(user_bp)

# 3.定义类视图[passport.py]


# 4.自定义返回的json格式
from utils.output import output_json

# 装饰器representation拦截底层返回的字典，自定义json格式
user_api.representation(mediatype="application/json")(output_json)

# 5.给类视图添加路由信息
# /app/sms/codes
# http://127.0.0.1:8000/app/sms/codes/18512341234
from app.resources.user.passport import SMSCodeResource,LoginRegisterResource

user_api.add_resource(SMSCodeResource, '/sms/codes/<mob:mobile>')
# /app/authorizations
user_api.add_resource(LoginRegisterResource,'/authorizations')
# 6在app中注册蓝图对象[app.__init__文件]

