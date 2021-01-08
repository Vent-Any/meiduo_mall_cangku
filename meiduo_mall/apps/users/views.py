from django.shortcuts import render

# Create your views here.
from django.views import View
from django_redis import get_redis_connection

from apps.users.models import User, Address
from django.http import JsonResponse
import json
from django import http
import re
from utils.views import LoginRequiredJsonMixin
from apps.users.utils import generate_verify_email_url, check_verify_email_token


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
        body = request.body  # request.body 是byte类型
        body_str = body.decode()  # byte转字符串
        data = json.loads(body_str)  # 字符串转字典
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


class LoginView(View):
    def post(self, request):
        """"
        1 接受参数
        data = json.loads(request.body.decode())
        2 提取参数
        username = data.get('username')
        password = data.get('password')
        remembered = data.get('remembered')
        3 检验参数
        if not all([username, password]):
            return JsonResponse({'code':400,'errmsg':"参数不全"})
        4 认证登录用户
            # django自带admin后台，admin 可以验证用户名和密码
            # django 实现了用户名和密码的验证方法。
            from django.contrib.auth import authentucate, login
            user = authenticate(username=username, password=password)
            if user is None:
                return JsonResponse({'code':400, 'errmsg':"用户名和密码错误"})
        5 状态保持
            login(request,user)
        6 要根据是否记住登录
            if remembered:
                 request.session.set_expiry(None)
            else:
                request.session.set_expiry(0)
        7 返回响应
            return JsonResponse({'code':0, 'errmsg':"OK"})
        """
        from django.contrib.auth import authenticate, login
        data = json.loads(request.body.decode())
        username = data.get('username')
        password = data.get('password')
        remembered = data.get('remembered')
        # 使用正则进行username的判断，是用户名还是手机号
        # 如果是手机号，就将USERNAME_FIELD改为mobile  USERNAME_FIELD 规定了根据什么来进行验证。
        if re.match('1[3-9]\d{9}', username):
            User.USERNAME_FIELD = 'mobile'
        # 如果不是手机号就是用户名，将USERNAME_FIELD设置为username
        else:
            User.USERNAME_FIELD = 'username'
        # 验证参数
        if not all([username, password]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({'code': 400, 'errmsg': '用户名或者密码不正确'})
        # user不为 None 可以进行状态保持。
        login(request, user)
        if remembered:
            request.session.set_expiry(None)
        else:
            request.session.set_expiry(0)
        response = JsonResponse({'code': 0, 'errmsg': "OK"})
        response.set_cookie('username', username, max_age=14 * 24 * 3600)
        return response


class LogoutView(View):
    def delete(self, request):
        # 删除状态保持信息
        from django.contrib.auth import logout
        logout(request)
        # 删除cookie
        response = JsonResponse({'code': 0, 'errmsg': 'OK'})
        response.delete_cookie('username')
        return response


#########################################################################
from utils.views import LoginRequiredJsonMixin

"""
LoginRequiredMixin ： 判断用户是否登录
authenticate：  判断用户名和密码是否正确
"""


# View 直接将dispatch走完了 不会调用LoginRequiredMixin的dispatch
# 先进性有没有登录的判断。　先执行LoginRequiredMixin 的dispatch


class UserInfoView(LoginRequiredJsonMixin, View):
    def get(self, request):
        # request 里面有一个user属性,这个user 属性是系统根据我们的Session信息自动帮我们添加的.
        # 如果我们真的的登录了request.user 就是我们数据库中的那个实例对象
        user = request.user
        user_info = {
            'username': user.username,
            'mobile': user.mobile,
            'email': user.email,
            'email_active': user.email_active,
        }
        return JsonResponse({'code': 0, 'errmsg': "OK", 'info_data': user_info})


class EmailView(View):
    """添加邮箱"""

    def put(self, request):
        """实现添加邮箱逻辑"""
        # 接收参数
        json_dict = json.loads(request.body.decode())
        email = json_dict.get('email')

        # 校验参数
        if not email:
            return http.JsonResponse({'code': 400,
                                      'errmsg': '缺少email参数'})
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return http.JsonResponse({'code': 400,
                                      'errmsg': '参数email有误'})

        # django发送邮件服务器设置
        # 发送激活邮件
        # from django.core.mail import send_mail
        # subject = '主题'
        # message = ''
        # from_email = '美多商城<qi_rui_hua@163.com>'
        # recipient_list = [email]
        # html_message = '<a href="#">点击激活</a>'
        # send_mail(
        #     subject,
        #     message,
        #     from_email,
        #     recipient_list,
        #     html_message,
        #  )
        from celery_tasks.email.tasks import send_verify_email
        verify_url = generate_verify_email_url(request.user)
        send_verify_email.delay(email, verify_url)
        # 赋值email字段
        user = request.user
        user.email = email
        user.save()
        # 响应添加邮箱结果
        return http.JsonResponse({'code': 0, 'errmsg': '添加邮箱成功'})


class VerifyEmailView(View):
    def put(self, request):
        # - 1.接收 token
        token = request.GET.get('token')
        if not token:
            return JsonResponse({'code': 400, 'errmsg': 'token缺少'})

        # - 2.解密

        data_dict = check_verify_email_token(token)

        # - 4.去数据库对比 user_id,email
        try:
            user = User.objects.get(id=data_dict)
        except:
            return JsonResponse({'code': 400, 'errmsg': '参数有误!'})
        # - 5.修改激活状态
        user.email_active = True
        user.save()
        return JsonResponse({'code': 0, 'errmsg': 'ok'})


class CreateAddressView(LoginRequiredJsonMixin, View):

    def post(self,request):
        """
        1. 必须是登录用户才可以新增地址
        2. 接收参数
        3. 提取参数
        4. 验证参数 (省略--作业)
        5. 数据入库
        6. 返回响应
        :param request:
        :return:
        """
        # 1. 必须是登录用户才可以新增地址   LoginRequiredJSONMixin
        # 2. 接收参数
        data = json.loads(request.body.decode())

        # 3. 提取参数(课件copy)
        receiver = data.get('receiver')
        province_id = data.get('province_id')
        city_id = data.get('city_id')
        district_id = data.get('district_id')
        place = data.get('place')
        mobile = data.get('mobile')
        tel = data.get('tel')
        email = data.get('email')

        # 4. 验证参数 (省略--作业)
        # 5. 数据入库
        address = Address.objects.create(
            user=request.user,
            title=receiver,
            receiver=receiver,
            province_id=province_id,
            city_id=city_id,
            district_id=district_id,
            place=place,
            mobile=mobile,
            tel=tel,
            email=email
        )
        # 6. 返回响应
        address_dict = {
            'id':address.id,
             "title": address.title,
            "receiver": address.receiver,
            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email
        }

        return JsonResponse({'code':0,'errmsg':'ok','address': address_dict})


    #######################
class AddressesListView(View):
    def get(self, request):
        """
        1 必须是登录用户可以获取地址

        :param request:
        :return:
        """
        addresses = Address.objects.filter(user=request.user, is_deleted=False)
        # 创建空的列表
        address_dict_list = []
        # 遍历
        for address in addresses:
            address_dict = {
                "id": address.id,
                "title": address.title,
                "receiver": address.receiver,
                "province": address.province.name,
                "city": address.city.name,
                "district": address.district.name,
                "place": address.place,
                "mobile": address.mobile,
                "tel": address.tel,
                "email": address.email
            }
            address_dict_list.append(address_dict)

        default_id = request.user.default_address_id

        return JsonResponse({'code': 0,
                             'errmsg': 'ok',
                             'addresses': address_dict_list,
                             'default_address_id': default_id})
