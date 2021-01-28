from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from apps.goods.models import SKU
from apps.meiduo_admin.serializer import sku
from apps.meiduo_admin.serializer.sku import GoodCategoryModelSerializer
from apps.meiduo_admin.utils import PageNumber


class SKUModelSetView(ModelViewSet):
    queryset = SKU.objects.all()
    serializer_class = sku.SKUModelSerializer
    pagination_class = PageNumber


from apps.goods.models import GoodsCategory
from rest_framework.views import APIView


class GoodsCategoryApiView(APIView):
    def get(self, request):
        gcs = GoodsCategory.objects.filter(subs=None)
        s = GoodCategoryModelSerializer(instance=gcs, many=True)
        return Response(s.data)


# SPU
from apps.goods.models import SPU
from rest_framework.generics import ListAPIView
from apps.meiduo_admin.serializer.sku import SimpleSPUModelSerializer


class SimpleListView(ListAPIView):
    queryset = SPU.objects.all()
    serializer_class = SimpleSPUModelSerializer


####################################################################
from apps.goods.models import SPUSpecification, SpecificationOption  # 规格和选项
from apps.meiduo_admin.serializer.sku import SPUSpecModelSerializer


class GoodsSpecAPIView(APIView):
    def get(self, requeset, spu_id):
        specs = SPUSpecification.objects.filter(spu_id=spu_id)
        s = SPUSpecModelSerializer(instance=specs, many=True)
        return Response(s.data)
