"""

消费者   执行任务
    通过指令来消费任务（执行函数）
    虚拟环境下 celery -A celery实例对象的文件路径 worker -l  INFO
"""
from celery import Celery
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo_mall.settings")
# 1 、创建实例
# celery 的第一个参数main其实就是一个名字
# 名字一般使用任务的名字（没有什么作用。）
app = Celery(main='meiduo')

# 2、加载celery 的配置信息
# 配置信息中指定了我们的broker（消息队列）
# 我们选择redis作为消息队列（broker）
# 我们把broker 的配置单独放到一个文件中，让celery加载这个文件
# 因为以后我们还有其他的配置。最好单独创建一个配置文件。
app.config_from_object('celery_tasks.config')

# app.autodiscover_tasks([])   tasks 是列表。
app.autodiscover_tasks(['celery_tasks.sms', 'celery_tasks.email'])
