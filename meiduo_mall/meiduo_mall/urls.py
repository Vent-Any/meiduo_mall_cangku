"""meiduo_mall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import path, include, register_converter
from django.contrib import admin
# 导入日志类
import logging
# 根据配置信息,创建日志器
from django.http import HttpResponse


def test(request):
    logger = logging.getLogger('django')
    # 记录日志
    # 如果有警告
    logger.warning('这里有一个警告')
    # 如果有错误
    logger.error('error')
    # 如果是记录信息
    logger.info('123')
    return HttpResponse('test')


# 注册我们的转换器
from utils.converters import *

# 参数1 转换器类
# 参数2 起别名
register_converter(UsernameConverter, 'uc')
register_converter(MobileConverter, 'mb')
register_converter(UUIDConverter, 'uuid')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('test/', test),
    path('', include('apps.users.urls')),
    path('', include('apps.verifications.urls')),
    path('', include('apps.oauth.urls')),
    path('', include('apps.areas.urls')),
    path('', include('apps.goods.urls')),
    path('', include('apps.carts.urls')),
    path('', include('apps.orders.urls')),
]
