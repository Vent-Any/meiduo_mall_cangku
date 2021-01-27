from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from apps.meiduo_admin.views import home, users, image
from . import login
urlpatterns = [
    path('authorizations/', login.admin_obtain_token),
    path('statistical/day_active/',home.UserActiveAPIView.as_view()),
    path('statistical/day_order/',home.UserOrderAPIView.as_view()),
    path('statistical/month_increment/',home.UserMonthAPiView.as_view()),
    path('users/',users.UserListAPIView.as_view()),
    path('skus/simple/',image.SimpleSKUListAPIView.as_view()),
]
from rest_framework.routers import DefaultRouter
router =DefaultRouter()
router.register('skus/images',image.ImageModelViewSet,basename='images')
urlpatterns += router.urls