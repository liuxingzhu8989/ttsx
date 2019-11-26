from django.shortcuts import render
from goods.models import GoodsType, IndexGoodsBanner, IndexTypeGoodsBanner,IndexPromotionBanner
from django.views.generic import View

# Create your views here.

class IndexView(View):
    def get(self, request):
        types = GoodsType.objects.all()
        goods_banners = IndexGoodsBanner.objects.all()
        type_goods_banners = IndexTypeGoodsBanner.objects.all()
        promotion_banners = IndexPromotionBanner.objects.all()
        context = {'types':types,
                    'goods_banners': goods_banners,
                    'type_goods_banners': type_goods_banners,
                    'promotion_banners':promotion_banners,
                  }

        return render(request, 'index.html', context)

    def post(self, request):
        pass
