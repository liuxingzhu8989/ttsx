1. 更改urls.py

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi apps/cart/urls.py 
   ```

   #urls.py

   ```
   from cart.views import CartAddView, CartShowView, CartUpdateView, CartDeleteView #add CartDeleteView
   
   app_name = 'cart'
   urlpatterns = [
       path('add', CartAddView.as_view(), name='add'),
       path('show', CartShowView.as_view(), name='show'),
       path('update', CartUpdateView.as_view(), name='update'),
       path('delete'. CartDeleteView.as_view(), name = 'delete'), #add delete
   ]
   ```

2. 更改views.py

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi apps/cart/views.py 
   ```

   #views.py

   ```
   class CartDeleteView(View):
       '''购物车记录删除'''
       def post(self, request):
           '''购物车记录删除'''
           user = request.user
           if not user.is_authenticated:
               # 用户未登录
               return JsonResponse({'res': 0, 'errmsg': '请先登录'})
   
           # 接收参数
           sku_id = request.POST.get('sku_id')
   
           # 数据的校验
           if not sku_id:
               return JsonResponse({'res':1, 'errmsg':'无效的商品id'})
   
           # 校验商品是否存在
           try:
               sku = GoodsSKU.objects.get(id=sku_id)
           except GoodsSKU.DoesNotExist:
               # 商品不存在
               return JsonResponse({'res':2, 'errmsg':'商品不存在'})
   
           # 业务处理:删除购物车记录
           conn = get_redis_connection('default')
           cart_key = 'cart_%d'%user.id
   
           # 删除 hdel
           conn.hdel(cart_key, sku_id)
   
           # 计算用户购物车中商品的总件数 {'1':5, '2':3}
           total_count = 0
           vals = conn.hvals(cart_key)
           for val in vals:
               total_count += int(val)
   
           # 返回应答
           return JsonResponse({'res':3, 'total_count':total_count, 'message':'删除成功'})
   ```

   