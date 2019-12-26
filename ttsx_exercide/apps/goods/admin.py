from django.contrib import admin
from goods.models import Goods,GoodsType,GoodsSKU,IndexPromotionBanner,IndexGoodsBanner,IndexTypeGoodsBanner

class GoodsAdmin(admin.ModelAdmin):
    fields = ('name','detail')
    list_display=('name', 'detail')

class GoodsTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

class GoodsSKUAdmin(admin.ModelAdmin):
    list_display = ('type', 'goods','name', 'desc', 'price','unite', 'stock')

class GoodsSKUType(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Goods, GoodsAdmin)
admin.site.register(GoodsType)
admin.site.register(GoodsSKU, GoodsSKUAdmin)
admin.site.register(IndexGoodsBanner)
admin.site.register(IndexTypeGoodsBanner)
admin.site.register(IndexPromotionBanner)
