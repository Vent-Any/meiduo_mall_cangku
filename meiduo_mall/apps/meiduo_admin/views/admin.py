from rest_framework.viewsets import ModelViewSet
from apps.users.models import User
from apps.meiduo_admin.serializer.admin import UserModelSerializer
from apps.meiduo_admin.utils import PageNumber
class AdminModelViewSet(ModelViewSet):
    queryset =User.objects.filter(is_staff=1)
    serializer_class =UserModelSerializer
    pagination_class = PageNumber



from rest_framework.generics import ListAPIView
from django.contrib.auth.models import Group
from apps.meiduo_admin.serializer.admin import GroupModelSerializer
class GruoplistModelView(ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupModelSerializer