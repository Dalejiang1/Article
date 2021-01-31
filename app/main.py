#启动项目文件
from app import create_app
from flask import jsonify

# 1创建app对象
app=create_app('dev')

# 2定义函数 绑定路由
@app.route('/')
def index():

    rule_dict={rule.rule:rule.endpoint for rule in app.url_map.iter_rules()}
    return jsonify(rule_dict)

if __name__ == '__main__':

    app.run(host='0.0.0.0',debug=True,port=5000)