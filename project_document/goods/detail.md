1. 添加order模型

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi apps/order/models.py 
   ```

   #models.py

   ```
   #goods detail
   from base_model.models import BaseModel
   
   class OrderInfo(BaseModel):
       '''订单模型类'''
       PAY_METHOD_CHOICES = (
           (1, '货到付款'),
           (2, '微信支付'),
           (3, '支付宝'),
           (4, '银联支付')
       )
   
       ORDER_STATUS_CHOICES = (
           (1, '待支付'),
           (2, '待发货'),
           (3, '待收货'),
           (4, '待评价'),
           (5, '已完成')
       )
   
       order_id = models.CharField(max_length=128, primary_key=True, verbose_name='订单id')
       user = models.ForeignKey('user.User', verbose_name='用户', on_delete='CASCADE')
       addr = models.ForeignKey('user.Address', verbose_name='地址', on_delete='CASCADE')
       pay_method = models.SmallIntegerField(choices=PAY_METHOD_CHOICES, default=3, verbose_name='支付方式')
       total_count = models.IntegerField(default=1, verbose_name='商品数量')
       total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品总价')
       transit_price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='订单运费')
       order_status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, default=1, verbose_name='订单状态')
       trade_no = models.CharField(max_length=128, verbose_name='支付编号')
   
       class Meta:
           db_table = 'df_order_info'
           verbose_name = 'order_info_v'
           verbose_name_plural = 'order_info_p'
   
   # Create your models here.
   class OrderGoods(BaseModel):
       '''订单商品模型类'''
       order = models.ForeignKey('OrderInfo', verbose_name='订单', on_delete='CASCADE')
       sku = models.ForeignKey('goods.GoodsSKU', verbose_name='商品SKU', on_delete='CASCADE')
       count = models.IntegerField(default=1, verbose_name='商品数目')
       price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
       comment = models.CharField(max_length=256, default='', verbose_name='评论')
   
       class Meta:
           db_table = 'df_order_goods'
           verbose_name = 'order_goods_v'
           verbose_name_plural = 'order_goods_p'
   ```

2. 修改html模板文件

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi templates/index.html 
   ```

   #index.html

   ```
   <li>
   {# add url lable in href #}
                       <h4><a href="{% url 'goods:detail' banner.sku.id %}">{{ banner.sku.name }}</a></h4> 
                       <a href="{% url 'goods:detail' banner.sku.id %}"><img src="{{ banner.sku.image.url }}"></a>
                       <div class="prize">¥ {{ banner.sku.price }}</div>
                   </li>
   ```

3. 修改views.py

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi apps/goods/views.py 
   ```

   #view.py

   ```
   #商品详情
   from order.models import OrderGoods
   
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
   ```

4. 修改urls.py

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi apps/goods/urls.py
   ```

   #urls.py

   ```
   from django.urls import path,re_path #add re_path
   
   urlpatterns = [
       path('index/', IndexView.as_view(), name ='index'),
       re_path('detail/(?P<goods_id>\d+)$', DetailView.as_view(), name ='detail'), #add re_path
   ]
   ```

   