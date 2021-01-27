from rest_framework.generics import ListAPIView
from rest_framework.generics import ListCreateAPIView
from apps.meiduo_admin.serializer.users import UserModelSerializer
from apps.users.models import User
from apps.meiduo_admin.utils import PageNumber



class UserListAPIView(ListCreateAPIView):
    # queryset = User.objects.all()
    # queryset = User.objects.filter(username_contains = keyword)
    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        if keyword:
            return User.objects.filter(username__contains=keyword)
        else:
            return User.objects.all()

    serializer_class = UserModelSerializer
    pagination_class = PageNumber
