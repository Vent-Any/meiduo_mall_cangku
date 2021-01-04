from django.shortcuts import render

# Create your views here.
from django.views import View
from django_redis import get_redis_connection

from apps.users.models import User
from django.http import JsonResponse
import json
from django import http
import re


class UsernameCountView(View):
    """判断用户名是否重复注册"""

    def get(self, request, username):
        """
        :param request: 请求对象
        :param username: 用户名
        :return: JSON
        """
        # 根据username 进行数量的查询.
        count = User.objects.filter(username=username).count()
        # 将结果进行返回.
        return JsonResponse({'code': 400, 'errmsg': 'OK', 'count': count})

class MobileCountView(View):
    """判断手机号是否重复注册"""

    def get(self, request, mobile):
        """
        :param request: 请求对象
        :param mobile: 手机号
        :return: JSON
        """
        count = User.objects.filter(mobile=mobile).count()
        return JsonResponse({'code': 0, 'errmsg': 'OK', 'count': count})


########################################################
class RegisterView(View):
    def post(self, request):
        """
        1 接受请求
        2 提取参数
        3 验证参数
        4 保存参数
        5 状态保持
        6返回响应
        :param request:
        :return:
        """
        # 1 接受请求
        body = request.body     # request.body 是byte类型
        body_str = body.decode()    #  byte转字符串
        data = json.loads(body_str)  #  字符串转字典
        username = data.get('username')
        password = data.get('password')
        password2 = data.get('password2')
        mobile = data.get('mobile')
        allow = data.get('allow')
        sms_code = data.get('sms_code')

        # 2 验证参数
        # 变量必须有值
        # 验证密码和用户名和手机号是否规范
        # 判断两次密码一样.

        # 判断参数是否齐全
        if not all([username, password, password2, mobile, allow]):
            return http.JsonResponse({'code': 400, 'errmsg': '缺少必传参数!'})
        # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9_]{5,20}$', username):
            return http.JsonResponse({'code': 400, 'errmsg': 'username格式有误!'})
        # 判断密码是否是8-20个数字
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.JsonResponse({'code': 400, 'errmsg': 'password格式有误!'})
        # 判断两次密码是否一致
        if password != password2:
            return http.JsonResponse({'code': 400, 'errmsg': '两次输入不对!'})
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.JsonResponse({'code': 400, 'errmsg': 'mobile格式有误!'})
        # 判断是否勾选用户协议
        if allow != True:
            return http.JsonResponse({'code': 400, 'errmsg': 'allow格式有误!'})
        # 判断手机验证码是否正确。
        redis_conn = get_redis_connection('code')
        sms_code_server = redis_conn.get('sms_%s' % mobile)
        print(sms_code_server)
        if sms_code_server is None:
            # 手机验证码过期或者不存在
            return JsonResponse({'code': 400, 'errmsg': '手机验证码失效'})
        elif sms_code_server.decode() != sms_code:
            return JsonResponse({'code': 400, 'errmsg': '手机验证码失效'})

        # 保存参数
        # user = User(username=username,password=password,mobile=mobile)
        # user.save()
        # user = User.objects.create(username=username,password=password,mobile=mobile)
        # 上面两种方法不能实现密码的加密
        # 使用User.objects.create_user  可以对用户密码进行加密.
        user = User.objects.create_user(username=username,
                                        password=password,
                                        mobile=mobile)

        # 状态保持
        # request.session['id']= user.id
        # request.session['username']= user.username
        # request.session['mobile']= user.mobile
        from django.contrib.auth import login
        # 参数一  请求对象
        # 参数二  用户信息
        login(request, user)

        # 返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok'})
