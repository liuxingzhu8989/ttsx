from django.shortcuts import render, redirect
from django.views.generic import View
from goods.models import GoodsType, GoodsSKU, IndexGoodsBanner,IndexPromotionBanner,IndexTypeGoodsBanner
from django_redis import get_redis_connection

#缓存
from django.core.cache import cache

#商品详情
from order.models import OrderGoods

class IndexView(View):
    def get(self, request):
        context = cache.get('index_page')
        if not context:
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

            context = {'types': types,
                       'goods_banners': goods_banners,
                       'promotion_banners': promotion_banners}

            cache.set('index_page', context)

        cart_count = 0

        conn = get_redis_connection('default')
        user = request.user
        if user.is_authenticated:
            cart_key = 'cart_%d'%user.id 
            cart_count = conn.hlen(cart_key)

        context.update(cart_count=cart_count) 
        return render(request, 'index.html', context)

class DetailView(View):
    def get(self, request, goods_id):
        try:
            sku = GoodsSKU.objects.get(id=goods_id)
        except GoodsSKU.DoesNotExist:
            return redirect(reverse("goods:detail"))

        # 获取商品的分类信息
        types = GoodsType.objects.all()
        
        # 获取商品的评论信息
        sku_orders = OrderGoods.objects.filter(sku=sku).exclude(comment='')

        # 获取新品信息
        new_skus = GoodsSKU.objects.filter(type=sku.type).order_by('-create_time')[:2]

        # 获取同一个SPU的其他规格商品
        same_spu_skus = GoodsSKU.objects.filter(goods=sku.goods).exclude(id=goods_id)
        
        user = request.user
        cart_count = 0 
        if user.is_authenticated:
            # 用户已登录
            conn = get_redis_connection('default')
            cart_key = 'cart_%d' % user.id
            cart_count = conn.hlen(cart_key)

            # 添加用户的历史记录
            conn = get_redis_connection('default')
            history_key = 'history_%d'%user.id
            # 移除列表中的goods_id
            conn.lrem(history_key, 0, goods_id)
            # 把goods_id插入到列表的左侧
            conn.lpush(history_key, goods_id)
            # 只保存用户最新浏览的5条信息
            conn.ltrim(history_key, 0, 4)    

        context = {'sku':sku, 'types': types,
                   'sku_orders':sku_orders,
                   'new_skus':new_skus,
                   'same_spu_skus':same_spu_skus,
                   'cart_count':cart_count}

        return render(request, 'detail.html', context)
