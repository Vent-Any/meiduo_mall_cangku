from django.http import JsonResponse
from django.shortcuts import render
from QQLoginTool.QQtool import OAuthQQ
from apps.oauth.models import OAuthQQUser
# Create your views here.
from django.views import View
import json


class QQUserView(View):
    def get(self, request):
        # 获取code
        code = request.GET.get('code')
        if code is None:
            return JsonResponse({'code': 400, 'errmsg': '没有参数'})
        """
        client_id = None    我们在创建应用的时候的id
        client_secret = None  我们在创建应用的时候的密钥
        redirect_uri = None  当我们用户同意之后,跳转的页面的url
        """
        # QQ登录参数
        # 我们申请的 客户端id
        QQ_CLIENT_ID = '101474184'
        # 我们申请的 客户端秘钥
        QQ_CLIENT_SECRET = 'c6ce949e04e12ecc909ae6a8b09b637c'
        # 我们申请时添加的: 登录成功后回调的路径
        QQ_REDIRECT_URI = 'http://www.meiduo.site:8080/oauth_callback.html'
        qq = OAuthQQ(
            client_id=QQ_CLIENT_ID,
            client_secret=QQ_CLIENT_SECRET,
            redirect_uri=QQ_REDIRECT_URI)
        # 通过code换取access_token
        access_token = qq.get_access_token(code)
        # 通过access_token 换取openid
        openid = qq.get_open_id(access_token)
        try:
            qquser = OAuthQQUser.objects.get(openid=openid)

        except OAuthQQUser.DoesNotExist:
            return JsonResponse({'code': 300, 'access_token': openid})
            pass
        else:
            from django.contrib.auth import login
            login(request, qquser.user)

            response = JsonResponse({'code': 0, 'errmsg': "OK"})
            response.set_cookie('username', qquser.user.username, max_age=14 * 24 * 3600)
            return response

    def post(self, request):
        # 接受请求
        data = json.loads(request.body.decode())
        # 获取参数
        mobile = data.get('mobile')
        password = data.get('password')
        sms_code = data.get('sms_code')
        openid = data.get('access_token')
        # 验证参数
        # 1 必须都有值
        # 2 手机号是否规则
        # 3 验证码是否规则
        # 4 短信验证码是否符合
        # 根据手机号判断用户信息
        from apps.users.models import User
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            # 如果没有查询到,新增信息
            user = User.objects.create_user(username=mobile,
                                            mobile=mobile,
                                            password=password)
        else:
            if not user.check_password(password):
                return JsonResponse({'code': 0, 'errmsg': "绑定失败"})
        # 查到了,进行绑定
        from apps.oauth.models import OAuthQQUser
        OAuthQQUser.objects.create(openid=openid, user=user)
        # 状态保持
        from django.contrib.auth import login
        login(request, user)
        # 设置cookie
        response = JsonResponse({'code': 0, 'errmsg': 'Ok'})
        response.set_cookie('username', user.username, max_age=14 * 24 * 3600)
        # 返回响应
        return response


