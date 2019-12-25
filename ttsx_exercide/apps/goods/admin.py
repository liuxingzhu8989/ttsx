from django.contrib import admin
from goods.models import Goods,GoodsType,IndexPromotionBanner,IndexGoodsBanner,IndexTypeGoodsBanner

admin.site.register(Goods)
admin.site.register(GoodsType)
admin.site.register(IndexGoodsBanner)
admin.site.register(IndexTypeGoodsBanner)
admin.site.register(IndexPromotionBanner)
