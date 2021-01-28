from apps.goods.models import SKU
from rest_framework import serializers

################################保存#############################
from apps.goods.models import SKUSpecification, SKU


class SKUSpecificationModelSerializer(serializers.ModelSerializer):
    spec_id = serializers.IntegerField()
    option_id = serializers.IntegerField()

    class Meta:
        model = SKUSpecification
        fields = ['spec_id', 'option_id']


class SKUModelSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField()
    category = serializers.StringRelatedField()
    specs = SKUSpecificationModelSerializer(many=True)
    spu_id = serializers.IntegerField()
    spu = serializers.StringRelatedField()

    class Meta:
        model = SKU
        fields = '__all__'

    def create(self, validated_data):
        specs = validated_data.pop('specs')
        from django.db import transaction
        with transaction.atomic():
            save_point = transaction.savepoint()
            try:
                sku = SKU.objects.create(**validated_data)
                for spec in specs:
                    SKUSpecification.objects.create(sku=sku, **spec)
            except Exception:
                transaction.savepoint_rollback(save_point)

            else:
                transaction.savepoint_commit(save_point)
        return sku

    def update(self, instance, validated_data):
        # 1 把一对多的数据pop
        specs = validated_data.pop('specs')
        # 2 只剩下剩余数据
        super().update(instance,validated_data)
        # 3 遍历多的数据进行更新
        for spec in specs:
            # 不支持修改规格
            SKUSpecification.objects.filter(sku=instance, spec_id=spec.get('spec_id')).update(
                option_id=spec.get('option_id'))
        return instance


##########################################################
"""
1 获取三级分类
"""
from apps.goods.models import GoodsCategory


class GoodCategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = ['id', 'name']


from apps.goods.models import SPU


class SimpleSPUModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SPU
        fields = ['id', 'name']


############################################################
from apps.goods.models import SPUSpecification, SpecificationOption


class SPUOptionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificationOption
        fields = ['id', 'value']


class SPUSpecModelSerializer(serializers.ModelSerializer):
    spu = serializers.StringRelatedField()
    spu_id = serializers.IntegerField()
    options = SPUOptionModelSerializer(many=True)

    class Meta:
        model = SPUSpecification
        fields = ['id', 'name', 'spu', 'spu_id', 'options']
