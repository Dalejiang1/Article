# app的初始化文件

from flask import Flask
from redis import StrictRedis
from flask_migrate import Migrate
from app.settings.config import config_dict
from flask_sqlalchemy import SQLAlchemy

# 需求：将common设置为资源文件，添加到搜索路径中
import os, sys

# 项目根路径：/Users/chenqian/Desktop/深圳41期Flask项目/HMTopNews
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# /Users/chenqian/Desktop/深圳41期Flask项目/HMTopNews/common
common_path = os.path.join(base_path, "common")
# 添加到搜索路径中
sys.path.insert(0, common_path)

# 去掉common资源路径
from utils.constants import EXTRA_ENV_COINFIG

#创建mysql数据库对象
db=SQLAlchemy()
#创建redis客户端数据库对象
redis_client=None #type:StrictRedis






def _create_app(config_name):
    """

    # 内部调用-创建app对象的工厂方法
    :param config_name:  配置类的名称 [dev  pro  test]
    :return: app
    """

    # 1.创建app对象
    app = Flask(__name__)

    # 获取配置类
    config_class = config_dict[config_name]
    # 2.从配置类中读取配置信息
    app.config.from_object(config_class)

    # 3.从环境变量中读取配置信息
    # export ENV_CONFIG 配置文件路径
    # silent=True 即使没有配置也不会报错
    app.config.from_envvar(EXTRA_ENV_COINFIG, silent=True)




    # 4.返回app对象
    return app




def create_app(config_name):
    """
        给外界调用的工厂方法生产app对象
        :return: app
        """
    # 1调用内部工厂方法创建app对象

    app=_create_app(config_name)

    #TODO 2添加依赖于app扩展组件

    register_extensions(app)


    # TODO 3注册蓝图
    register_blueprints(app)


    return app

def register_extensions(app:Flask):

    """组件初始化"""
    """
       注册依赖于app的拓展组件
       :param app: 应用对象
       :return:
       
       """
# 1延后加载app关联数据库对象
    db.init_app(app)
# 2延后创建redis客户端对象给‘全局变量’赋值
    global redis_client
# 懒加载
    # decode_responses=True 将返回的bytes类型数据解码成字符串
    redis_client = StrictRedis(host=app.config["REDIS_HOST"],
                               port=app.config["REDIS_PORT"],
                               decode_responses=True)

    # 3 添加自定义路由转换器
    from utils.converters import MobileConverter
    app.url_map.converters['mob']=MobileConverter

    # 4.添加迁移功能
    # No changes in schema detected. 模型文件未被发现，原因：user.py文件被孤立了
    # TODO：注意：一定要导入user模块才能迁移成功
    from models import user
    Migrate(app, db)

def register_blueprints(app:Flask):
    """
    注册蓝图
    :param app:应用对象
    :return:
    """
    #延后导包 防止循环导包
    from app.resources.user import user_bp
    # 1注册用户模型的蓝图对象
    app.register_blueprint(user_bp)


