1. 修改urls.py

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi apps/order/urls.py 
   ```

   #urls.py

   ```
   from order.views import OrderPlaceView, OrderCommitView #add OrderCommitView
   
   app_name = 'order'
   urlpatterns = [
       path('place', OrderPlaceView.as_view(), name='place'),
       path('commit', OrderCommitView.as_view(), name='commit'), #add commit
   ]
   ```
   
2. 更改views.py

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi apps/order/views.py
   ```

   #views.py

   ```
   from django.shortcuts import render, redirect
   from django.http import JsonResponse
   from order.models import OrderInfo,OrderGoods
   from datetime import datetime
   
   class OrderCommitView(View):
       '''订单创建'''
       def post(self, request):
           '''订单创建'''
           # 判断用户是否登录
           user = request.user
           if not user.is_authenticated:
               # 用户未登录
               return JsonResponse({'res':0, 'errmsg':'用户未登录'})
   
           # 接收参数
           addr_id = request.POST.get('addr_id')
           pay_method = request.POST.get('pay_method')
           sku_ids = request.POST.get('sku_ids') # 1,3
   
           # 校验参数
           if not all([addr_id, pay_method, sku_ids]):
               return JsonResponse({'res':1, 'errmsg':'参数不完整'})
   
           # 校验支付方式
           if pay_method not in OrderInfo.PAY_METHODS.keys():
               return JsonResponse({'res':2, 'errmsg':'非法的支付方式'})
   
           # 校验地址
           try:
               addr = Address.objects.get(id=addr_id)
           except Address.DoesNotExist:
               # 地址不存在
               return JsonResponse({'res':3, 'errmsg':'地址非法'})
   
           # todo: 创建订单核心业务
   
           # 组织参数
           # 订单id: 20171122181630+用户id
           order_id = datetime.now().strftime('%Y%m%d%H%M%S')+str(user.id)
   
           # 运费
           transit_price = 10
   
           # 总数目和总金额
           total_count = 0
           total_price = 0
   
           # todo: 向df_order_info表中添加一条记录
           order = OrderInfo.objects.create(order_id=order_id,
                                            user=user,
                                            addr=addr,
                                            pay_method=pay_method,
                                            total_count=total_count,
                                            total_price=total_price,
                                            transit_price=transit_price)
   
           # todo: 用户的订单中有几个商品，需要向df_order_goods表中加入几条记录
           conn = get_redis_connection('default')
           cart_key = 'cart_%d'%user.id
   
           sku_ids = sku_ids.split(',')
           for sku_id in sku_ids:
               # 获取商品的信息
               try:
                   sku = GoodsSKU.objects.get(id=sku_id)
               except:
                   # 商品不存在
                   return JsonResponse({'res':4, 'errmsg':'商品不存在'})
   
               # 从redis中获取用户所要购买的商品的数量
               count = conn.hget(cart_key, sku_id)
   
               # todo: 向df_order_goods表中添加一条记录
               OrderGoods.objects.create(order=order,
                                         sku=sku,
                                         count=count,
                                         price=sku.price)
   
               # todo: 更新商品的库存和销量
               sku.stock -= int(count)
               sku.sales += int(count)
               sku.save()
   
               # todo: 累加计算订单商品的总数量和总价格
               amount = sku.price*int(count)
               total_count += int(count)
               total_price += amount
   
           # todo: 更新订单信息表中的商品的总数量和总价格
           order.total_count = total_count
           order.total_price = total_price
           order.save()
   
           # todo: 清除用户购物车中对应的记录
           conn.hdel(cart_key, *sku_ids)
   
           # 返回应答
           return JsonResponse({'res':5, 'message':'创建成功'})
   ```

   