
class BaseConfig(object):
    """默认配置"""

    """配置父类"""
    # 取消中文编码
    JSON_AS_ASCII = False

    # 加密字符串
    SECRET_KEY = "python41"

    # mysql配置
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:mysql@192.168.248.157:3306/python41'  # 连接地址
    #多库连接配置信息
    #SQLALCHEMY_BINDS = {}

    # 关闭数据库修改跟踪操作
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True  # 是否打印底层执行的SQL
    # 自动提交：db.session.commmit()
    # SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # redis配置
    REDIS_HOST = '192.168.248.157'  # ip
    REDIS_PORT = 6381  # 端口

    # JWT配置信息
    JWT_SECRET='TPmi4aLWRbyVq8zu9v82dWYW17/z+UvRnYTt4P6fAXA'
    JWT_EXPIRE_DAYS=14


    # 读取配置信息方法：app.config.get("REDIS_HOST")


class DevelopmentConfig(BaseConfig):
    """开发环境配置类"""
    pass


class ProductionConfig(BaseConfig):
    """生产环境配置类"""
    pass


class TestingConfig(BaseConfig):
    """测试环境配置类"""
    pass


# 提供一个字典给被的模块调用
config_dict = {
    "dev": DevelopmentConfig,
    "pro": ProductionConfig,
    "test": TestingConfig
}
