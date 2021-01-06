from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from apps.areas.models import Area

class ProvienceView(View):
    def get(self, request):
        province_model_list = Area.objects.filter(parent__isnull=True)

        province_list = []
        for province_model in province_model_list:
            province_list.append({'id': province_model.id, 'name': province_model.name})

        return JsonResponse({'code': 0, 'errmsg': 'OK', 'province_list': province_list})