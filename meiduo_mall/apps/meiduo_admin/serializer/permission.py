from django.contrib.auth.models import Permission
from django.contrib.auth.models import ContentType

"""
权限: 是否可以进行后台登录
登录后台系统的权限
    实际上还是对模型的增删改查
"""
from django.contrib.auth.models import Permission
from rest_framework import serializers

class PermissionModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = '__all__'