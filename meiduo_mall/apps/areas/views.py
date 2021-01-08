from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from apps.areas.models import Area


class ProvienceView(View):
    def get(self, request):

        from django.core.cache import cache
        cache.delete('province')
        province_list = cache.get('province')
        if province_list is None:
            province_model_list = Area.objects.filter(parent=None)
            province_list = []
            for province_model in province_model_list:
                province_list.append({'id': province_model.id,
                                      'name': province_model.name})
            cache.set('province', province_list, 24 * 3600)

        return JsonResponse({'code': 0, 'errmsg': 'OK', 'province_list': province_list})


class SubAreaView(View):
    # pk 是前端传递的参数 parent_id
    def get(self, request, pk):
        """
        1 接受参数
        2 根据parent_id进行查询
        3 遍历结果集
        4 返回响应
        :param request: 
        :param pk: 
        :return: 
        """
        from django.core.cache import cache
        subs_list = cache.get('sub_area_%s' %pk)
        if subs_list is None:
            subs_areas = Area.objects.filter(parent_id=pk)
            subs_list = []
            for item in subs_areas:
                subs_list.append({
                    'id': item.id,
                    'name': item.name
                })
            cache.set('sub_area_%s' % pk, subs_list, 24 * 3600)

        return JsonResponse({'code': 0, 'errmsg': 'ok', 'sub_data': {'subs': subs_list}})
