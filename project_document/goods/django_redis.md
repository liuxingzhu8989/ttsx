[参考文档](https://django-redis-chs.readthedocs.io/zh_CN/latest/)

1. 用django-redis作为cache缓存浏览记录

   安装django-redis

   ```
   (venv) [ms@localhost ttsx_exercide]$ pip install django-redis
   ```

   修改settings.py

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi ttsx_exercide/settings.py 
   ```

   #settings.py

   ```
   CACHES = {
       "default": {
           "BACKEND": "django_redis.cache.RedisCache",
           "LOCATION": "redis://127.0.0.1:6379/1",
           "OPTIONS": {
               "CLIENT_CLASS": "django_redis.client.DefaultClient",
           }
       }
   }
   ```

2. 使用

   语法

   ```
   from django_redis import get_redis_connection
   con = get_redis_connection("default") #default 对应到settings.py的default
   ```

   修改app/user/views.py

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi apps/user/views.py 
   ```

   #views

   ```
   #/user/info
   class InfoView(LoginRequiredMixin, View):
       def get(self, request):
           ...
           history_key = 'history_user%d'%user.id
           sku_ids = con.lrange(history_key, 0, 4)
           
           goods_li = []
           for id in sku_ids:
               goods = GoodsSKU.objects.get(id=id)
               goods_li.append(goods)
   
           return render(request, user_info, {'page':'info', 'address':address, 'good_li':goods_li}) #add goods list
   ```

   #TODO

