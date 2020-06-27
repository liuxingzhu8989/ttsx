1. 修改views.py

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi apps/order/views.py 
   ```

   #views.py

   ```
   from django.db import transaction
   
   
   class OrderCommitView(View):
       '''订单创建'''
       @transaction.atomic
       def post(self, request):
       
       # 设置事务保存点
           save_id = transaction.savepoint()
           try:
               # todo: 向df_order_info表中添加一条记录
               order = OrderInfo.objects.create(order_id=order_id,
           ...
           except Exception as e:
           	transaction.savepoint_rollback(save_id)
           transaction.savepoint_commit(save_id)
   ```

2. 修改mysql配置

   ```
   (venv) [ms@localhost ~]$ sudo vi /etc/my.cnf
   ```

   #my.cnf

   ```
   transaction_isolation = READ-COMMITTED
   ```

   