from haystack import indexes
from apps.goods.models import SKU

class SKUIndex(indexes.SearchIndex,indexes.Indexable):
    #属性
    # 模型很像
    text = indexes.CharField(document=True, use_template=True)



    # 对那个模型类进行检索  返回类名就可以
    def get_model(self):
        return SKU

    # 要对那些数据进行检索
    def index_queryset(self, using=None):
        # 返回查询结果集
        return self.get_model().objects.filter(is_launched=True)