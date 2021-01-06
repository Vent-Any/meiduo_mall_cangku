from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from  itsdangerous import BadSignature
# 创建实例对象
s = Serializer(secret_key='123', expires_in=3600)
# 组织数据然后加密
data = {
    'openid':'abc123'
}
# 加密
s.dumps(data)

"""
解密数据
"""
# 导入(同上)
# 创建实例对象
# 解密数据
# data =s.dump(data)
# try:
#   s.loads(data)
# except BadSignature:
#   print('数据改了')