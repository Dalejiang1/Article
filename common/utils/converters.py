from werkzeug.routing import BaseConverter
# 需求: 192.168.248.157:5000/mobile/131112341234  提取路径上的手机号码，要求手机号码满足正则表达式规则


class MobileConverter(BaseConverter):
    # .重写父类的regex属性，将手机号码正则表达式给予其赋值
    # 注意：不需要匹配开头 ^

    regex = "1[3-9]\d{9}$"
