from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings
from apps.users.models import User

def generate_verify_email_url(user):
    """
    生成邮箱验证链接
    :param user: 当前登录用户
    :return: verify_url
    """
    serializer = Serializer(settings.SECRET_KEY, expires_in=3600)
    data = {'user_id': user.id, 'email': user.email}
    token = serializer.dumps(data).decode()
    verify_url = settings.EMAIL_VERIFY_URL + '?token=' + token
    return  verify_url


def check_verify_email_token(token):
    """
    验证token并提取user
    :param token: 用户信息签名后的结果
    :return: user, None
    """
    serializer = Serializer(settings.SECRET_KEY, expires_in=3600)
    data = serializer.loads(token)
    user_id = data.get('user_id')
    email = data.get('email')
    user = User.objects.get(id=user_id, email=email)
    return user