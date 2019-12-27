from django.db import models
from base_model.models import BaseModel
from tinymce.models import HTMLField

class GoodsType(BaseModel):
    '''商品类型'''
    name = models.CharField(max_length=20)
    logo = models.CharField(max_length=20)
    image = models.ImageField(upload_to='type')

    class Meta:
        db_table = 'df_goods_type'
        verbose_name = '商品类型'
        verbose_name_plural = '商品类型s'

    def __str__(self):
        return str(self.name)


class GoodsSKU(BaseModel):
    '''商品SKU'''
    status_choices = (
        (0, '下线'),
        (1, '上线'),
    )
    type = models.ForeignKey('GoodsType', on_delete='CASCADE')
    goods = models.ForeignKey('Goods', on_delete='CASCADE')
    name = models.CharField(max_length=20)
    desc = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unite = models.CharField(max_length=20)
    image = models.ImageField(upload_to='goods')
    stock = models.IntegerField(default=1)
    sales = models.IntegerField(default=0)
    status = models.SmallIntegerField(default=1, choices=status_choices)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'df_goods_sku'
        verbose_name = '商品sku'
        verbose_name_plural = '商品skus'


class Goods(BaseModel):
    '''商品SPU'''
    name = models.CharField(max_length=20)
    # 富文本类型:带有格式的文本
    detail = HTMLField(blank=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'df_goods'
        verbose_name = '商品spu'
        verbose_name_plural = '商品spus'


class GoodsImage(BaseModel):
    '''商品图片'''
    sku = models.ForeignKey('GoodsSKU', on_delete='CASCADE')
    image = models.ImageField(upload_to='goods')

    class Meta:
        db_table = 'df_goods_image'
        verbose_name = '商品图片'
        verbose_name_plural = '商品图片s'


class IndexGoodsBanner(BaseModel):
    '''首页轮播商品展示'''
    sku = models.ForeignKey('GoodsSKU', on_delete='CASCADE')
    image = models.ImageField(upload_to='banner')
    index = models.SmallIntegerField(default=0) # 0 1 2 3

    def __str__(self):
        return str(self.sku)

    class Meta:
        db_table = 'df_index_banner'
        verbose_name = 'index_goods_banner_v'
        verbose_name_plural = 'index_goods_banner_p'


class IndexTypeGoodsBanner(BaseModel):
    '''首页分类商品展示'''
    DISPLAY_TYPE_CHOICES = (
        (0, "标题"),
        (1, "图片")
    )

    type = models.ForeignKey('GoodsType', on_delete='CASCADE')
    sku = models.ForeignKey('GoodsSKU', on_delete='CASCADE')
    display_type = models.SmallIntegerField(default=0, choices=DISPLAY_TYPE_CHOICES)
    index = models.SmallIntegerField(default=0)

    def __str__(self):
        return str(self.type) + "_" + str(self.sku) + "_" + str(self.DISPLAY_TYPE_CHOICES[self.display_type][1])

    class Meta:
        db_table = 'df_index_type_goods'
        verbose_name = "index_type_goods_v"
        verbose_name_plural = 'index_type_goods_p'


class IndexPromotionBanner(BaseModel):
    '''首页促销活动'''
    name = models.CharField(max_length=20)
    url = models.CharField(max_length=256)
    image = models.ImageField(upload_to='banner')
    index = models.SmallIntegerField(default=0)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'df_index_promotion'
        verbose_name = "index_promotion_v"
        verbose_name_plural = 'index_promotion_p'
