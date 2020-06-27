1. 添加urls.py

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi ttsx_exercide/urls.py
   ```

   #urls.py

   ```
   urlpatterns = [
       ...
       path('cart/', include('cart.urls'), name = 'cart'),
   ]
   ```

   修改cart/urls.py

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi apps/cart/urls.py
   ```

   #urls.py

   ```
   from django.urls import path
   from cart.views import CartAddView
   urlpatterns = [
   	path('add/', CartAddView.as_view(), name='add'),
   ]
   ```

2. 修改views.py

   ```
   from django.http import JsonResponse
   class CartAddView(View):
       def post(self, request):
           user = request.user
           if not user.is_authenticated:
               return JsonResponse({'res':0, 'errmsg':'please login first'})
   
           #校验数据
           sku_id = request.POST.get('sku_id')
           count = request.POST.get('count')
   
           if not all((sku_id, count)):
               return JsonResponse({'res':1, 'errmsg':'data is not integral'})
   
           #校验商品数量
           try:
               count = int(count)
           except Exception as e:
               return JsonResponse({'res':2, 'errmsg':'goods value is wrong'})
   
           try:
               sku = GoodsSKU.objects.get(id=sku_id)
           except GoodsSKU.DoesNotExist:
               return JsonResponse({'res':3, 'errmsg':'goods does not exsit'})
   
           conn = get_redis_connection('default')
           cart_key = 'cart_%d'%user.id
           cart_count = conn.hget(cart_key, sku_id)
           if cart_count:
               count += int(cart_count)
   
           # 校验商品的库存
           if count > sku.stock:
               return JsonResponse({'res':4, 'errmsg':'商品库存不足'})
   
           # 设置hash中sku_id对应的值
           # hset->如果sku_id已经存在，更新数据， 如果sku_id不存在，添加数据
           conn.hset(cart_key, sku_id, count)
   
            # 计算用户购物车商品的条目数
           total_count = conn.hlen(cart_key)
           # 返回应答
           return JsonResponse({'res':5, 'total_count':total_count, 'message':'添加成功'})
```
   
   