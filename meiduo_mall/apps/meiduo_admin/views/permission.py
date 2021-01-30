from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import Permission
from apps.meiduo_admin.utils import PageNumber
from apps.meiduo_admin.serializer.permission import PermissionModelSerializer


class PermissionModelView(ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionModelSerializer
    pagination_class = PageNumber