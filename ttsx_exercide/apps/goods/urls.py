from django.urls import path,re_path
from goods.views import IndexView, DetailView

app_name = 'goods'
urlpatterns = [
    path('index/', IndexView.as_view(), name ='index'),
    re_path('detail/(?P<goods_id>\d+)$', DetailView.as_view(), name ='detail'),
]
