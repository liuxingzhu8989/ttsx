1. 更新urls.py

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi apps/cart/urls.py 
   ```

   #urls.py

   ```
   from cart.views import CartAddView, CartShowView #add CartShowView
   
   app_name = 'cart'
   urlpatterns = [
       path('add', CartAddView.as_view(), name='add'),
       path('show', CartShowView.as_view(), name='show'), #add show
   ]
   ```

2. 更新views.py

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi apps/cart/views.py 
   ```

   #views.py

   ```
   #/cart/show
   class CartShowView(View):
       def get(self, request):
           '''显示'''
           # 获取登录的用户
           user = request.user
           # 获取用户购物车中商品的信息
           conn = get_redis_connection('default')
           cart_key = 'cart_%d'%user.id
           # {'商品id':商品数量, ...}
           
           cart_dict = conn.hgetall(cart_key)
   
           skus = []
           # 保存用户购物车中商品的总数目和总价格
           total_count = 0
           total_price = 0
           # 遍历获取商品的信息
           for sku_id, count in cart_dict.items():
               # 根据商品的id获取商品的信息
               sku = GoodsSKU.objects.get(id=sku_id)
               # 计算商品的小计
               amount = sku.price*int(count)
               # 动态给sku对象增加一个属性amount, 保存商品的小计
               sku.amount = amount
               # 动态给sku对象增加一个属性count, 保存购物车中对应商品的数量
               sku.count = int(count)
               # 添加
               skus.append(sku)
   
               # 累加计算商品的总数目和总价格
               total_count += int(count)
               total_price += amount
   
           # 组织上下文
           context = {'total_count':total_count,
                      'total_price':total_price,
                      'skus':skus}
           return render(request, 'cart.html', context)
   ```

   