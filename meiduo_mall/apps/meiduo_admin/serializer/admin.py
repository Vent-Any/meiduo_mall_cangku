from django.contrib.auth.models import Group

from apps.users.models import User
from rest_framework import serializers
class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','mobile']

    def create(self, validated_data):
        # 我们的组和权限  没有添加
        # user = User.objects.create_user()
        user = super().create(validated_data)
        user.set_password(validated_data.get('password'))
        user.is_staff = True
        user.save()

        return user

class GroupModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
