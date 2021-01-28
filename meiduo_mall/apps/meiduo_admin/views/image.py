from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from apps.goods.models import SKUImage
from apps.meiduo_admin.serializer.image import SKUImageModelSerializer
from apps.meiduo_admin.utils import PageNumber


class ImageModelViewSet(ModelViewSet):
    queryset = SKUImage.objects.all()
    serializer_class = SKUImageModelSerializer
    pagination_class = PageNumber

    def create(self, request, *args, **kwargs):
        upload_image = request.FILES.get('image')
        sku_id = request.data.get('sku')
        try:
            sku = SKU.objects.get(id=sku_id)
        except:
            return Response({'msg': '没有此商品'})
        # 4.图片上传七牛云,我们把七牛云给我们返回的图片名字保存到数据库
        from qiniu import Auth, put_data, etag
        # 需要填写你的 Access Key 和 Secret Key
        access_key = 'q9crPZPROOXrykaH85q_zpEEll0f_LsjXwUnXHRo'
        secret_key = 'lG_4_tI8bJTR8Zk6z8fGwYp79aQHkJgolvvBL_qm'
        # 构建鉴权对象
        q = Auth(access_key, secret_key)
        # 要上传的空间
        bucket_name = 'shunyi44'
        # 上传后保存的文件名--使用系统,我们不使用
        key = None
        # 生成上传 Token，可以指定过期时间等
        token = q.upload_token(bucket_name, key, 3600)
        # 要上传二进制数据
        # 读取图片的二进制
        data = upload_image.read()
        # ret 结果
        # info 上传信息
        ret, info = put_data(token, key, data=data)
        # ret['key']是自动生成的图片名字
        image_url = ret['key']
        new_image = SKUImage.objects.create(
            sku_id=sku_id,
            image=image_url
        )
        return Response({
            'id': new_image.id,
            'image': new_image.image.url,
            'sku': sku_id
        }, status=201)


    def update(self, request, *args, **kwargs):
        data = request.data
        sku_id = data.get('sku')
        new_upload_image = data.get('image')
        try:
            sku = SKU.objects.get(id=sku_id)
        except:
            return Response({'msg': '没有此商品'})
            # 4.图片上传七牛云,我们把七牛云给我们返回的图片名字保存到数据库
        from qiniu import Auth, put_data, etag
        # 需要填写你的 Access Key 和 Secret Key
        access_key = 'q9crPZPROOXrykaH85q_zpEEll0f_LsjXwUnXHRo'
        secret_key = 'lG_4_tI8bJTR8Zk6z8fGwYp79aQHkJgolvvBL_qm'
        # 构建鉴权对象
        q = Auth(access_key, secret_key)
        # 要上传的空间
        bucket_name = 'shunyi44'
        # 上传后保存的文件名--使用系统,我们不使用
        key = None
        # 生成上传 Token，可以指定过期时间等
        token = q.upload_token(bucket_name, key, 3600)
        # 要上传二进制数据
        # 读取图片的二进制
        data = new_upload_image.read()
        # ret 结果
        # info 上传信息
        ret, info = put_data(token, key, data=data)
        # ret['key']是自动生成的图片名字
        new_image_url = ret['key']
        pk = self.kwargs.get('pk')
        new_image  = SKUImage.objects.get(id=pk)
        new_image.image = new_image_url
        new_image.save()
        return Response({
            'id':new_image.id,
            'image':new_image.image.url,
            'sku':sku_id
        })


from rest_framework.generics import ListAPIView
from apps.goods.models import SKU
from apps.meiduo_admin.serializer.image import SimpleSKUModelSerializer


class SimpleSKUListAPIView(ListAPIView):
    queryset = SKU.objects.all()
    serializer_class = SimpleSKUModelSerializer
