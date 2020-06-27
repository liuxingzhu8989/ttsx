1. 安装

   ```
   pip install django-redis-session=0.5.6
   ```

2. 默认数据库

   ```
   #SESSION_ENGINE='django.contrib.sessions.backends.cache'
   #SESSION_ENGINE='django.contrib.sessions.backends.db'
   #SESSION_ENGINE='django.contrib.sessions.backends.cached_db'
   ```

3. Redis存储，在settings.py配置

   ```
   SESSION_ENGINE = 'redis_sessions.session'
   SESSION_REDIS_HOST = 'localhost'
   SESSION_REDIS_PORT = 6379
   SESSION_REDIS_DB = 2
   SESSION_REDIS_PASSWORD = ''
   SESSION_REDIS_PREFIX = 'session'
   ```

4. 用法

   ```
   request.session[key] = 'value'
   ```

   