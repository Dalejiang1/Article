class BaseConfig(object):

    """配置父类"""
    # 取消中文编码
    JSON_AS_ASCII = False

    # 加密字符串
    SECRET_KEY = "python41"


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
