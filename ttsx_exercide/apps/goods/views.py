from django.shortcuts import render
from django.views.generic import View
from goods.models import GoodsType, GoodsSKU, IndexGoodsBanner,IndexPromotionBanner,IndexTypeGoodsBanner
from django_redis import get_redis_connection

class IndexView(View):
    def get(self, request):
        types = GoodsType.objects.all()  
        # 获取首页轮播商品信息
        goods_banners = IndexGoodsBanner.objects.all()
        # 获取首页促销活动信息
        promotion_banners = IndexPromotionBanner.objects.all().order_by('index')
        
        for type in types: # GoodsType
                # 获取type种类首页分类商品的图片展示信息
                image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by('index')
                # 获取type种类首页分类商品的文字展示信息
                title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by('index')

                # 动态给type增加属性，分别保存首页分类商品的图片展示信息和文字展示信息
                type.image_banners = image_banners
                type.title_banners = title_banners

        cart_count = 0

        conn = get_redis_connection('default')
        user = request.user
        if user.is_authenticated:
            cart_key = 'cart_%d'%user.id 
            cart_count = conn.hlen(cart_key)

        context = {'types': types,
                   'goods_banners': goods_banners,
                   'promotion_banners': promotion_banners,
                   'cart_count':cart_count}
        
        return render(request, 'index.html', context)


