from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import HttpResponse, JsonResponse


class ImageCodeView(View):
    def get(self, request, uuid):
        # 1、接受请求
        # 2、获取数据
        # 3、验证参数
        #  还是应用自定义转换器。即 converters.
        # 4、生成图片和获取验证内容
        from libs.captcha.captcha import captcha
        # captcha 返回两个参数   其中一个是内容  一个是图片二进制。
        text, image =captcha.generate_captcha()
        # 5、保存图片验证码
        # 先连接redis
        from django_redis import get_redis_connection
        # get_redis_connection（配置中的名字）
        # 获取redis链接
        redis_cli = get_redis_connection('code')
        redis_cli.setex(uuid, 300, text)
        # 6、返回响应
        # 告诉浏览器 我们返回的是二进制。
        return HttpResponse(image, content_type='image/jpeg')


class SmsCodeView(View):
    def get(self, request, mobile):

        """
        1.接收参数
        2.获取参数
        3.验证参数(作业课下补齐)
        4.提取redis中的图片验证码
        5.把redis中的图片验证码删除
        6.用户的图片验证码和reids进行比对
            (redis的数据是bytes类型的,内容大小写统一)
        7. 通过程序生成短信验证码
        8. 将短信验证码保存到redis中
        9. 通过荣联云 发送短信
        10. 返回响应
        :param request:
        :param mobile:
        :return:
        """
        # 1.接收参数 (手机号,用户的图片验证码,uuid)
        # 2.获取参数
        # /sms_codes/<mobile>/?image_code=xxxx&image_code_id=xxxx

        # request.GET           1   查询字符串
        # request.POST          2   (form表单数据)
        # request.body          3  (JSON)
        # request.META          4 (请求头)
        # 用户的图片验证码
        image_code=request.GET.get('image_code')
        uuid=request.GET.get('image_code_id')
        # 3.验证参数(作业课下补齐)
        # 3.1 这2个变量 都要有数据
        # 3.2 image_code 的长度
        # 3.3 uuid

        # 4.提取redis中的图片验证码
        from django_redis import get_redis_connection
        redis_cli=get_redis_connection('code')

        redis_text=redis_cli.get(uuid)

        # 5.把redis中的图片验证码删除
        redis_cli.delete(uuid)

        # 6.用户的图片验证码和reids进行比对
        #     (redis的数据是bytes类型的,内容大小写统一)

        # 用户输入的  和 redis中的 不相等 就用户输错了
        # redis_text.decode() 将bytes类型 转换为 str
        # 内容大小写统一
        if image_code.lower() !=  redis_text.decode().lower():
            return JsonResponse({'code':400,'errmsg':'图片验证码错误'})
        send_flag = redis_cli.get('send_flag_%s' % mobile)
        if send_flag:
            return JsonResponse({'code': 400, 'errmsg': '发送短信过于频繁'})

        # 7. 通过程序生成短信验证码
        from random import randint

        sms_code=randint(100000,999999)

        # 8. 将短信验证码保存到redis中
        # setex key seconds value
        # 10分钟过期  600s
        # 创建Redis管道
        pl = redis_cli.pipeline()
        # 将Redis请求添加到队列
        pl.setex('sms_%s' % mobile, 300, sms_code)
        pl.setex('send_flag_%s' % mobile, 60, 1)
        # 执行请求
        pl.execute()

        # 9. 通过荣联云 发送短信
        from ronglian_sms_sdk import SmsSDK
        accId = '8a216da8762cb4570176c60593ba35ec'
        accToken = '514a8783b8c2481ebbeb6a814434796f'
        appId = '8a216da8762cb4570176c605948c35f2'

        # 9.1. 创建荣联云 实例对象
        sdk = SmsSDK(accId, accToken, appId)
        tid = '1'  # 我们发送短信的模板,值 只能是 1 因为我们是测试用户
        mobile = '%s'%mobile  # '手机号1,手机号2'    给哪些手机号发送验证码,只能是测试手机号
        datas = (sms_code, 10)  # ('变量1', '变量2')  涉及到模板的变量
        # 您的验证码为{1},请于{2} 分钟内输入
        # 您的验证码为666999,请于5 分钟内输入
        # 9.2. 发送短信
        sdk.sendMessage(tid, mobile, datas)

        # 10. 返回响应
        return JsonResponse({'code':0,'errmsg':'ok'})
