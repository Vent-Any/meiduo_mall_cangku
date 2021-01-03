from ronglian_sms_sdk import SmsSDK

accId = '8a216da8762cb4570176c60593ba35ec'
accToken = '514a8783b8c2481ebbeb6a814434796f'
appId = '8a216da8762cb4570176c605948c35f2'

def send_message():
    # 创建容联云 实例对象
    sdk = SmsSDK(accId, accToken, appId)
    tid = '1'    # 这个是发送的短信模板  只能是1
    mobile = '17614321583'        # 给那些手机发送验证码，只能是测试手机号。
    datas = ('666', 5)     # 您的验证码为{1}请于{2}分钟内输入。
    # 发送验证短信。
    resp = sdk.sendMessage(tid, mobile, datas)
    print(resp)

# 调用函数
send_message()