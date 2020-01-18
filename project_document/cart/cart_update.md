1. 更新urls.py

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi apps/cart/urls.py 
   ```

   #urls.py

   ```
   from cart.views import CartAddView, CartShowView, CartUpdateView.as_view
   
   app_name = 'cart'
   urlpatterns = [
       path('add', CartAddView.as_view(), name='add'),
       path('show', CartShowView.as_view(), name='show'),
       path('update', CartUpdateView.as_view(), name='update'), #add the line
   ]
   ```

2. 更新views.py

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi apps/cart/views.py 
   ```

   #views.py

   ```
   class CartUpdateView(View):
       '''购物车记录更新'''
       def post(self, request):
           '''购物车记录更新'''
           user = request.user
           if not user.is_authenticated():
               # 用户未登录
               return JsonResponse({'res': 0, 'errmsg': '请先登录'})
   
           # 接收数据
           sku_id = request.POST.get('sku_id')
           count = request.POST.get('count')
   
           # 数据校验
           if not all([sku_id, count]):
               return JsonResponse({'res': 1, 'errmsg': '数据不完整'})
   
           # 校验添加的商品数量
           try:
               count = int(count)
           except Exception as e:
               # 数目出错
               return JsonResponse({'res': 2, 'errmsg': '商品数目出错'})
   
           # 校验商品是否存在
           try:
               sku = GoodsSKU.objects.get(id=sku_id)
           except GoodsSKU.DoesNotExist:
               # 商品不存在
               return JsonResponse({'res': 3, 'errmsg': '商品不存在'})
   
           # 业务处理:更新购物车记录
           conn = get_redis_connection('default')
           cart_key = 'cart_%d'%user.id
   
           # 校验商品的库存
           if count > sku.stock:
               return JsonResponse({'res':4, 'errmsg':'商品库存不足'})
   
           # 更新
           conn.hset(cart_key, sku_id, count)
   
           # 计算用户购物车中商品的总件数 {'1':5, '2':3}
           total_count = 0
           vals = conn.hvals(cart_key)
           for val in vals:
               total_count += int(val)
   
           # 返回应答
           return JsonResponse({'res':5, 'total_count':total_count, 'message':'更新成功'})
   ```

   