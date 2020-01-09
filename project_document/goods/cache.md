1. 安装django-redis

   ```
   pip install django-session
   pip install django-redis
   ```

2. 配置缓存，在settings.py

   
   
   #settings.py
   
   ```
   #django cache
   CACHES = {
       "default": {
           "BACKEND": "django_redis.cache.RedisCache",
           "LOCATION": "redis://127.0.0.1:6379/1",
           "OPTIONS": {
               "CLIENT_CLASS": "django_redis.client.DefaultClient",
           }
       }
   }
   
   #django session
   SESSION_ENGINE = "django.contrib.sessions.backends.cache"
   SESSION_CACHE_ALIAS = "default"
   ```
   
3. 缓存数据

   ```
   #导入cache
   from django.core.cache import cache
   
   
   class IndexView(View):
       def get(self, request):
           context = cache.get('index_page') #add
           if not context:   #add 
               types = GoodsType.objects.all() 
               ...
               cache.set('index_page', context) #add
               ...
           context.update(cart_count=cart_count) #add
           return render(request, 'index.html', context)
   ```

4. 测试

   在if not context里面加log,打开http://127.0.0.1:9001/goods/index/ 页面,观察有log出现，再次刷新，无log

5. 更改model admin

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi apps/goods/admin.py 
   ```

   #admin.py

   ```
   #import package
   from django.core.cache import cache
   
   def delete_model(self, request, obj):
           super().delete_model(self, request, obj)
           generate_static_index.delay()
           
           #删除缓存
           cache.delete('index_page') #add
   ```

   


