# app的初始化文件
from flask import Flask
from app.settings.config import config_dict
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

    app=_create_app(config_name)

    #TODO 添加依赖于app扩展组件

    #TODO 注册蓝图

    return app
