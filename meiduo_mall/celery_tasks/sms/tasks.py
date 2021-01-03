from ronglian_sms_sdk import SmsSDK
from celery_tasks.main import app
# 写我们的任务（函数）
# 任务必须要celery的实例对象装饰器task装饰
# 任务包的任务需要celery调用自检检查函数。(在main里面写。)

@app.task
def celery_send_sms_code(mobile, sms_code):
    accId = '8a216da8762cb4570176c60593ba35ec'
    accToken = '514a8783b8c2481ebbeb6a814434796f'
    appId = '8a216da8762cb4570176c605948c35f2'

    # 9.1. 创建荣联云 实例对象
    sdk = SmsSDK(accId, accToken, appId)
    tid = '1'  # 我们发送短信的模板,值 只能是 1 因为我们是测试用户
    mobile = '%s' % mobile  # '手机号1,手机号2'    给哪些手机号发送验证码,只能是测试手机号
    datas = (sms_code, 10)  # ('变量1', '变量2')  涉及到模板的变量
    # 您的验证码为{1},请于{2} 分钟内输入
    # 您的验证码为666999,请于5 分钟内输入
    # 9.2. 发送短信
    sdk.sendMessage(tid, mobile, datas)