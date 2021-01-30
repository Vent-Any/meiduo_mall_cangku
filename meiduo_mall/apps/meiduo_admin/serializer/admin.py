from apps.users.models import User
from rest_framework import serializers

class AdminModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'