from django.shortcuts import render
from goods.models import GoodsType, IndexGoodsBanner, IndexTypeGoodsBanner,IndexPromotionBanner
from django.views.generic import View
from django.core.cache import cache
from django_redis import get_redis_connection

# Create your views here.

class IndexView(View):
    def get(self, request):
        index_data = cache.get('index_data')
        cart_count = 0
        if index_data is None:
            print('here')
            types = GoodsType.objects.all()
            goods_banners = IndexGoodsBanner.objects.all()
            type_goods_banners = IndexTypeGoodsBanner.objects.all().order_by('index')
            promotion_banners = IndexPromotionBanner.objects.all().order_by('index')

            context = {'types':types,
                        'goods_banners': goods_banners,
                        'type_goods_banners': type_goods_banners,
                        'promotion_banners':promotion_banners,
                        'cart_count': cart_count,
                      }
            cache.set('index_data', context, 3600)
        else:
            print('already cache')

        user = request.user
        if user.is_authenticated:
            con = get_redis_connection('default')
            cart_key = 'cart_%d'%user.id
            cart_count = con.hlen(cart_key)


        index_data.update(cart_count=cart_count)
        return render(request, 'index.html', index_data)

    def post(self, request):
        pass
