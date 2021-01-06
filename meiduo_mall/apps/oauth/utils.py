from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from  itsdangerous import BadSignature

def generic_openid(openid):
    # 创建实例对象
    s = Serializer(secret_key='123', expires_in=3600)
    # 组织数据然后加密
    data = {
        'openid': openid
    }
    # 加密
    secret_data = s.dumps(data)
    return secret_data.decode()

"""
解密数据
"""
def check_token(token):
    s = Serializer(secret_key='123', expires_in=3600)
    # 导入(同上)
    # 创建实例对象
    # 解密数据
    try:
        data = s.loads(token)
    except BadSignature:
        return None

    return data.get('openid')