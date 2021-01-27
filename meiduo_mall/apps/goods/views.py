from django.http import JsonResponse
from django.shortcuts import render
from apps.goods.models import GoodsCategory, SKU
# Create your views here.
from django.views import View

from utils.goods import *


class IndexView(View):

    def get(self, request):
        """
        1. 获取分类数据
        2. 获取首页数据
        3. 组织数据 进行渲染
        :param request:
        :return:
        """
        # 1. 获取分类数据
        categories = get_categories()
        # 2. 获取首页数据
        contents = get_contents()
        # 3. 组织数据 进行渲染
        # 注意: key必须是这2个 因为模板中已经写死
        context = {
            'categories': categories,
            'contents': contents
        }
        return render(request, 'index.html', context)


# 列表视图
class ListView(View):
    def get(self, request, category_id):
        # 1 接受请求
        data = request.GET
        # 2 提取参数
        page = data.get('page')
        page_size = data.get('page_size')
        ordering = data.get('ordering')
        # 3 根据分类id查询数据
        from apps.goods.models import GoodsCategory
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except:
            return JsonResponse({'code': 400, 'errmsg': "没有此分类"})

        # 4 验证参数
        # 5 查询数据
        from apps.goods.models import SKU
        skus = SKU.objects.filter(category=category, is_launched=True).order_by(ordering)
        # 6 分页数据
        from django.core.paginator import Paginator
        paginator = Paginator(skus, per_page=page_size)
        page_skus = paginator.page(page)
        # 获取分了多少页
        total_num = paginator.num_pages
        # 将对象列表转换成字典
        sku_list = []
        for item in page_skus:
            sku_list.append({
                'id': item.id,
                'name': item.name,
                'price': item.price,
                'default_image_url': item.default_image.url
            })
        from utils.goods import get_breadcrumb
        breadcrumb = get_breadcrumb(category)
        # 返回响应
        return JsonResponse({'code': 0, 'errmsg': "ok", 'list': sku_list, 'count': total_num, 'breadcrumb': breadcrumb})


# 热销


class HotView(View):
    def get(self, request, category_id):
        """
        接收参数
        根据分类id查询数据
        查询sku数据
        将对象列表转换为字典
        返回响应
        :param request:
        :param category_id:
        :return:
        """
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except:
            return JsonResponse({'code': 400, 'errmsg': "没有此分类"})
        from apps.goods.models import SKU
        skus = SKU.objects.filter(category=category, is_launched=True).order_by('-sales')[0:2]
        sku_list = []
        for item in skus:
            sku_list.append({
                'id': item.id,
                'name': item.name,
                'price': item.price,
                'default_image_url': item.default_image.url
            })
        return JsonResponse({'code': 0, 'errmsg': "ok", 'hot_skus': sku_list})


from utils.goods import get_breadcrumb, get_categories, get_goods_specs


class DetailView(View):

    def get(self, request, sku_id):
        """
        1. 获取商品id
        2. 根据商品id查询商品信息
        3. 获取分类数据
        4. 获取面包屑数据
        5. 获取规格和规格选项数据
        6. 组织数据,进行HTML模板渲染
        7. 返回响应
        :param request:
        :param sku_id:
        :return:
        """
        # 1. 获取商品id
        # 2. 根据商品id查询商品信息
        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '没有此商品'})
        # 3. 获取分类数据
        categories = get_categories()
        # 4. 获取面包屑数据
        # sku 有 三级分类属性
        breadcrumb = get_breadcrumb(sku.category)
        # 5. 获取规格和规格选项数据
        # 传递 sku对象
        specs = get_goods_specs(sku)

        # 6. 组织数据,进行HTML模板渲染
        # context 的key 必须按照课件来!!!
        # 因为模板已经写死了
        context = {
            'sku': sku,
            'categories': categories,
            'breadcrumb': breadcrumb,
            'specs': specs
        }

        # 7. 返回响应
        return render(request, 'detail.html', context)


class CategoryVisitView(View):
    def post(self, request, category_id):
        """
        1 获取分类id
        2 查询分类数据
        3 我们查询数据库是否存在分类和日期的记录
        4 不存在新增
        5 存在修改
        """

        try:
            category = GoodsCategory.objects.get(id=category_id)
        except:
            return JsonResponse({'code': 400, 'errmsg': "没有此分类"})
        from datetime import date
        today = date.today()
        from apps.goods.models import GoodsVisitCount
        try:
            gvc = GoodsVisitCount.objects.get(category=category, date=today)
        except:
            GoodsVisitCount.objects.create(category=category, date=today, count=1)
        else:
            gvc.count += 1
            gvc.save()
        return JsonResponse({'code': 0, 'errmsg': 'OK'})


from haystack.views import SearchView


class MeiduoSearchView(SearchView):
    def create_response(self):
        # haystack 会接受请求帮助我们对接es
        # 这个时候数据已经获取到了
        context = self.get_context()
        page = context.get('page')
        object_list = page.object_list
        data_list = []
        for item in object_list:
            data_list.append({
                'id': item.object.id,
                'name': item.object.name,
                'price': item.object.price,
                'default_image_url':item.object.default_image.url,
                'searchkey': context.get('query'),
                "page_size": context.get('paginator').num_pages,
                "count": context.get('paginator').count
            })
        return JsonResponse(data_list, safe=False)
