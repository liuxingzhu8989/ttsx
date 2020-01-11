from django.shortcuts import render, redirect
from django.views.generic import View
from goods.models import GoodsType, GoodsSKU, IndexGoodsBanner,IndexPromotionBanner,IndexTypeGoodsBanner
from django_redis import get_redis_connection

#缓存
from django.core.cache import cache

#商品详情
from order.models import OrderGoods

#list信息
from django.core.paginator import Paginator 

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

class ListView(View):
    def get(self, request, type_id, page):
        #校验
        try:
            type = GoodsType.objects.get(id=type_id)
        except GoodsType.DoesNotExist:
            return redirect(reverse("goods:index"))
        

        #查询数据
        types = GoodsType.objects.all()
        sort = request.GET.get('sort')

        if sort == 'price':
            skus = GoodsSKU.objects.filter(type=type).order_by('price')
        elif sort == 'hot':
            skus = GoodsSKU.objects.filter(type=type).order_by('-sales')
        else:
            sort = 'default'
            skus = GoodsSKU.objects.filter(type=type).order_by('-id')
         
        #分页
        paginator = Paginator(skus, 1) 
        
        #获取指定页码内容
        ##页面校验,不合法
        try:
            cur_page = int(page)
        except Exception as e:
            cur_page = 1 

        #最大页面
        if cur_page > paginator.num_pages:
            cur_page = 1
        
        #获取指定页码对象
        skus_page = paginator.page(cur_page)

        #总页数小于5页，显示全部
        #当前页前3页，显示1-5
        #当前页后3页，显示后5页
        #显示当前页前2页，当前页，后两页
        num_pages = paginator.num_pages
        if num_pages < 5:
            pages = range(1,num_pages+1)
        elif cur_page <= 3:
            pages = range(1,6)
        elif num_pages - cur_page <= 2:
            pages = range(num_pages-4, num_pages+1)
        else:
            pages = range(cur_page-2, cur_page+3)

        # 获取新品信息
        new_skus = GoodsSKU.objects.filter(type=type).order_by('-create_time')[:2]
        
        user = request.user
        cart_count = 0
        if user.is_authenticated:
            # 用户已登录
            conn = get_redis_connection('default')
            cart_key = 'cart_%d' % user.id
            cart_count = conn.hlen(cart_key)

        context = {'type':type, 'types':types,
                   'skus_page': skus_page,
                   'new_skus': new_skus,
                   'pages': pages,
                   'cart_count': cart_count,}
 
        return render(request, 'list.html', context)
