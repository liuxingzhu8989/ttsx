from django.contrib import admin
from goods.models import GoodsType, GoodsSKU, Goods, GoodsImage, IndexGoodsBanner, IndexTypeGoodsBanner, IndexPromotionBanner
from django.core.cache import cache

class BaseTypeAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        from celery_tasks.tasks import generate_index_page
        generate_index_page.delay()
    
        cache.delete('index_data')

    def delete_mode(self, request, obj):
        super().delete_model(self, request, obj)

        from celery_tasks.tasks import generate_index_page
        generate_index_page.delay()
        
        cache.delete('index_data')

class IndexPromotionBannerAdmin(BaseTypeAdmin):
    pass

class IndexTypeGoodsBannerAdmin(BaseTypeAdmin):
    pass

# Register your models here.
admin.site.register(Goods)
admin.site.register(GoodsType)
admin.site.register(GoodsSKU)
admin.site.register(IndexGoodsBanner)
admin.site.register(IndexTypeGoodsBanner)
admin.site.register(IndexPromotionBanner, IndexPromotionBannerAdmin)

