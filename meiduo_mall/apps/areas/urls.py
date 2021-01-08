from django.urls import path
from apps.areas.views import *
urlpatterns = [
    # 获取省份
    path('areas/', ProvienceView.as_view()),
    # 市区县获取
    path('areas/<pk>/', SubAreaView.as_view()),
]