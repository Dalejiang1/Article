from redis import StrictRedis

# 创建redis客户端
# decode_responses=True 将返回的响应bytes类型数据解码成字符串
redis_client=StrictRedis(host='192.168.248.157',port=6381,decode_responses=True)

redis_client.set("name","curry",ex=3600)

print(redis_client.get('name'))
