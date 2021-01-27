from datetime import date
from rest_framework.response import Response

from apps.users.models import User
# # 获取今天date
# today = date.today
# # 过滤查询
# count = User.objects.filter(last_login_gte=today).count()


# 代码应该写入类视图
from rest_framework.views import APIView


class UserActiveAPIView(APIView):
    def get(self, request):
        # 获取今天date
        today = date.today()
        # 过滤查询
        count = User.objects.filter(last_login__gte=today).count()
        return Response({'count': count})


# 下单用户
class UserOrderAPIView(APIView):
    def get(self, request):
        today = date.today()
        count = User.objects.filter(orderinfo__create_time__gte=today)
        return Response({'count': count})


"""
1 返回的数据形式
2 我们先获取今天的日期,在获取三十天之前的日期进行遍历.
"""
from datetime import timedelta


class UserMonthAPiView(APIView):
    def get(self, request):
        today = date.today()
        befor_date = today - timedelta(days=30)
        data_list = []
        for i in range(0, 30):
            start_date = befor_date + timedelta(days=i)
            end_date =befor_date + timedelta(days=(i + 1))
            count = User.objects.filter(date_joined__gte=start_date, date_joined__gt=end_date).count()
            data_list.append({
                'count': count,
                'date': start_date
            })
        return Response(data_list)
