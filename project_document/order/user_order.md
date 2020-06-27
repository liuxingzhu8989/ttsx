1. 更改views.py

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi apps/user/views.py 
   ```

   #views.py

   ```
   from django.core.paginator import Paginator
   from order.models import OrderInfo,OrderGoods
   
   
   #/user/order
   class OrderView(LoginRequiredMixin,View):
       def get(self, request, page):
           '''显示'''
           # 获取用户的订单信息
           user = request.user
           orders = OrderInfo.objects.filter(user=user).order_by('-create_time')
   
           # 遍历获取订单商品的信息
           for order in orders:
               # 根据order_id查询订单商品信息
               order_skus = OrderGoods.objects.filter(order_id=order.order_id)
   
               # 遍历order_skus计算商品的小计
               for order_sku in order_skus:
                   # 计算小计
                   amount = order_sku.count*order_sku.price
                   # 动态给order_sku增加属性amount,保存订单商品的小计
                   order_sku.amount = amount
   
               # 动态给order增加属性，保存订单状态标题
               order.status_name = OrderInfo.ORDER_STATUS[order.order_status]
               # 动态给order增加属性，保存订单商品的信息
               order.order_skus = order_skus
   
           # 分页
           paginator = Paginator(orders, 1)
   
           # 获取第page页的内容
           try:
               page = int(page)
           except Exception as e:
               page = 1
   
           if page > paginator.num_pages:
               page = 1
   
           # 获取第page页的Page实例对象
           order_page = paginator.page(page)
   
           # todo: 进行页码的控制，页面上最多显示5个页码
           # 1.总页数小于5页，页面上显示所有页码
           # 2.如果当前页是前3页，显示1-5页
           # 3.如果当前页是后3页，显示后5页
           # 4.其他情况，显示当前页的前2页，当前页，当前页的后2页
           num_pages = paginator.num_pages
           if num_pages < 5:
               pages = range(1, num_pages + 1)
           elif page <= 3:
               pages = range(1, 6)
           elif num_pages - page <= 2:
               pages = range(num_pages - 4, num_pages + 1)
           else:
               pages = range(page - 2, page + 3)
               
           # 组织上下文
           context = {'order_page':order_page,
                      'pages':pages,
                      'page': 'order'}
   
           # 使用模板
           return render(request, 'user_center_order.html', context)
   ```

2. 修改urls.py

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi apps/user/urls.py 
   ```

   #urls.py

   ```
   re_path('order/(?P<page>\d+)$', OrderView.as_view(), name = 'order'), #add order
   ```

   