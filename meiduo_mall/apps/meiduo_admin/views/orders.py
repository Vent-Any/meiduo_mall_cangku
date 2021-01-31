from rest_framework.generics import ListAPIView

from apps.meiduo_admin.utils import PageNumber
from apps.orders.models import OrderInfo
from apps.meiduo_admin.serializer.orders import OrderListModelSerializer

class OrderListAPIView(ListAPIView):

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')

        if keyword:
            return OrderInfo.objects.filter(order_id=keyword)
        else:
            return OrderInfo.objects.all()

    serializer_class = OrderListModelSerializer

    pagination_class = PageNumber