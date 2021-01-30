from rest_framework.viewsets import ModelViewSet
from apps.users.models import User
from apps.meiduo_admin.serializer.admin import AdminModelSerializer
from apps.meiduo_admin.utils import PageNumber
class AdminModelViewSet(ModelViewSet):
    queryset =User.objects.filter(is_staff=1)
    serializer_class =AdminModelSerializer
    pagination_class = PageNumber