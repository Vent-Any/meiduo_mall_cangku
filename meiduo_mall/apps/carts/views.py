import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from django_redis import get_redis_connection

from apps.goods.models import SKU
from utils.views import LoginRequiredJsonMixin


class CartsView(LoginRequiredJsonMixin, View):
    def post(self, request):
        # 获取用户信息
        user = request.user
        # 接受参数
        data = json.loads(request.body.decode())
        # 提取参数
        sku_id = data.get('sku_id')
        count = data.get('count')
        # 验证参数
        if not all([sku_id, count]):
            return JsonResponse({'code': 400, 'errmsg': "参数不全"})
        try:
            sku = SKU.objects.get(id=sku_id)
        except:
            return JsonResponse({'code': 400, 'errmsg': "没有此商品"})
        try:
            count = int(count)
        except:
            count = 1
        redis_cli = get_redis_connection('carts')
        redis_cli.hset('carts_%s' % user.id, sku_id, count)
        redis_cli.sadd('selected_%s' % user.id, sku_id)
        return JsonResponse({'code': 0, 'errmsg': "OK"})

    def get(self, request):
        """
        0. 必须是登录用户,获取用户信息
        1. 连接redis
        2. 获取hash  {sku_id:count,sku_id:count}   key和value是 bytes
        3. 获取 set  {sku_id,sku_id}      选中商品id   value是 bytes
        4. 获取所有购物车中的商品id
        5. 遍历所有商品id 根据商品id查询商品信息
        6. 将对象转换为字典 (数量,选中状态和总价)
        7. 返回响应
        :param request:
        :return:
        """
        # 0. 必须是登录用户,获取用户信息
        user = request.user
        # 1. 连接redis
        redis_cli = get_redis_connection('carts')
        # 2. 获取hash  {sku_id:count,sku_id:count}   key和value是 bytes
        # 获取所有的 hash key 对应的数据是
        """
        HGETALL key
        返回哈希表 key 中，所有的域和值。
        """
        sku_id_counts = redis_cli.hgetall('carts_%s' % user.id)
        # {sku_id:count,sku_id:count}
        # 3. 获取 set  {sku_id,sku_id}      选中商品id   value是 bytes
        """
        SMEMBERS key
        返回集合 key 中的所有成员。
        不存在的 key 被视为空集合。
        """
        selected_ids = redis_cli.smembers('selected_%s' % user.id)
        # {sku_id,sku_id}
        # 4. 获取所有购物车中的商品id
        # 字典.keys() 获取字典的所有的key
        ids = sku_id_counts.keys()
        # [1,2,3]
        carts_sku = []
        # 5. 遍历所有商品id
        for id in ids:
            # 根据商品id查询商品信息
            sku = SKU.objects.get(id=id)
            # 6. 将对象转换为字典 (数量,选中状态和总价)
            carts_sku.append({
                'id': sku.id,
                'name': sku.name,
                'price': sku.price,
                'default_image_url': sku.default_image.url,
                'count': int(sku_id_counts[id]),  # 购物车数量   记得类型转换
                'selected': id in selected_ids,  # 选中状态   通过程序判断
                'amount': sku.price * int(sku_id_counts[id])  # 当前购物车中 数量*单价的 总价
            })
        # 7. 返回响应
        return JsonResponse({'code': 0, 'cart_skus': carts_sku, 'errmsg': 'ok'})

    def put(self, request):
        # 获取用户信息
        user = request.user
        # 接受请求
        data = json.loads(request.body.decode())
        # 获取数据
        sku_id = data.get('sku_id')
        count = data.get('count')
        selected = data.get('selected')
        # 验证数据
        try:
            sku = SKU.objects.get(id=sku_id)
        except:
            return JsonResponse({'code': 400, 'errmsg': "没有此商品"})
        # 连接数据库
        redis_cli = get_redis_connection('carts')
        redis_cli.hset('carts_%s' % user.id, sku_id, count)
        if selected:
            redis_cli.sadd('selected_%s' % user.id, sku_id)
        else:
            redis_cli.srem('selected_%s' % user.id, sku_id)
        # 返回响应  为了和前端数据保持一致

        cart_sku = {
            'id': sku.id,
            'name': sku.name,
            'price': sku.price,
            'count': count,  # 购物车数量   记得类型转换
            'selected': selected,  # 选中状态   通过程序判断
            'amount': sku.price * count  # 当前购物车中 数量*单价的 总价

        }
        return JsonResponse({'code': 0, 'errmsg': "OK", 'cart_sku': cart_sku})

    def delete(self, request):
        # 获取用户信息
        user = request.user
        # 接受参数
        data = json.loads(request.body.decode())
        # 提取数据
        sku_id = data.get('sku_id')
        # 验证参数
        try:
            sku = SKU.objects.get(id=sku_id)
        except:
            return JsonResponse({'code': 400, 'errmsg': "没有此商品"})
        # 链接数据库
        redis_cli = get_redis_connection('carts')
        # 删除数据
        redis_cli.hdel('carts_%s' % user.id, sku_id)
        redis_cli.srem('selected_%s' % user.id, sku_id)
        # 返回响应
        return JsonResponse({'code': 0, 'errmsg': "OK"})
