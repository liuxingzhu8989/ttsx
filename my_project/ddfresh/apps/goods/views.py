from django.shortcuts import render
from goods.models import GoodsType, IndexGoodsBanner, IndexTypeGoodsBanner,IndexPromotionBanner
from django.views.generic import View
from django_redis import get_redis_connection

# Create your views here.

class IndexView(View):
    def get(self, request):
        types = GoodsType.objects.all()
        goods_banners = IndexGoodsBanner.objects.all()
        type_goods_banners = IndexTypeGoodsBanner.objects.all()
        promotion_banners = IndexPromotionBanner.objects.all()

        cart_count = 0
        user = request.user
        if user.is_authenticated:
            con = get_redis_connection('default')
            cart_key = 'cart_%d'%user.id
            cart_count = con.hlen(cart_key)

        context = {'types':types,
                    'goods_banners': goods_banners,
                    'type_goods_banners': type_goods_banners,
                    'promotion_banners':promotion_banners,
                    'cart_count': cart_count,
                  }

        return render(request, 'index.html', context)

    def post(self, request):
        pass
