from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import Permission
from apps.meiduo_admin.utils import PageNumber

from apps.meiduo_admin.serializer.permission import PermissionModelSerializer


class PermissionModelView(ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionModelSerializer
    pagination_class = PageNumber


#########################权限的内容类型#######################

from django.contrib.auth.models import ContentType
from rest_framework.generics import ListAPIView
from apps.meiduo_admin.serializer.permission import  ContentTypeModelSerializer

class ContenTypeListAPIView(ListAPIView):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeModelSerializer
