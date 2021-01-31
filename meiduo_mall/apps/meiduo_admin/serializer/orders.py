from rest_framework.serializers import ModelSerializer
from apps.orders.models import OrderInfo


class OrderListModelSerializer(ModelSerializer):

    class Meta:
        model = OrderInfo
        fields = ['order_id', 'create_time']
