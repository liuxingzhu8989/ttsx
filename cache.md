1. 安装django-redis

   ```
   pip install django-session
   pip install django-redis
   ```

2. 配置缓存，在settings.py

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




 1. 浏览记录缓存

    >from django_redis import get_redis_connection
    >
    >con = get_redis_connection("default")