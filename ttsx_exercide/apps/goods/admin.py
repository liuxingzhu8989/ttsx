from django.contrib import admin
from goods.models import Goods,GoodsType,GoodsSKU,IndexPromotionBanner,IndexGoodsBanner,IndexTypeGoodsBanner

#celery 静态页面
from celery_tasks.tasks import generate_static_index

#删除缓存
from django.core.cache import cache

class GoodsAdmin(admin.ModelAdmin):
    fields = ('name','detail')
    list_display=('name', 'detail')

class GoodsTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

class GoodsSKUAdmin(admin.ModelAdmin):
    list_display = ('type', 'goods','name', 'desc', 'price','unite', 'stock')

class GoodsSKUType(admin.ModelAdmin):
    list_display = ('name',)

#类
class IndexPromotionBannerAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        generate_static_index.delay()

        #删除缓存
        cache.delete('index_page')

    def delete_model(self, request, obj):
        super().delete_model(self, request, obj)
        generate_static_index.delay()

        #删除缓存
        cache.delete('index_page')

admin.site.register(Goods, GoodsAdmin)
admin.site.register(GoodsType)
admin.site.register(GoodsSKU, GoodsSKUAdmin)
admin.site.register(IndexGoodsBanner)
admin.site.register(IndexTypeGoodsBanner)
admin.site.register(IndexPromotionBanner, IndexPromotionBannerAdmin)
