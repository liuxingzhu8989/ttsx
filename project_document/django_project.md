1. 生成project项目

   ```
   (venv) [ms@localhost ttsx_exercide]$ django-admin startproject ttsx_exercide .
   ```

2. 生成app

   ```
   #创建目录
   (venv) [ms@localhost ttsx_exercide]$ mkdir apps
   
   #创建user, goods, order, cart
   (venv) [ms@localhost ttsx_exercide]$ mkdir apps/user
   (venv) [ms@localhost ttsx_exercide]$ mkdir apps/goods
   (venv) [ms@localhost ttsx_exercide]$ mkdir apps/order
   (venv) [ms@localhost ttsx_exercide]$ mkdir apps/cart
   ==============================================================
   mkdir apps/user
   mkdir apps/goods
   mkdir apps/order
   mkdir apps/cart
   
   #创建app
   (venv) [ms@localhost ttsx_exercide]$ django-admin startapp user apps/user/
   (venv) [ms@localhost ttsx_exercide]$ django-admin startapp goods apps/goods/
   (venv) [ms@localhost ttsx_exercide]$ django-admin startapp order apps/order/
   (venv) [ms@localhost ttsx_exercide]$ django-admin startapp cart apps/cart/
   =========================================================================
   django-admin startapp user apps/user/
   django-admin startapp goods apps/goods/
   django-admin startapp order apps/order/
   django-admin startapp cart apps/cart/
   ```

3. 更改ttsx_exercide/settings.py

   ```
   #将app加入目录
   import sys
   sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
   
   INSTALLED_APPS = [
       ...
       'user',
       'goods',
       'cart',
       'order',
   ]
   
   #设置template文件夹
   TEMPLATES = [
       {
           ...
           'DIRS': [os.path.join(BASE_DIR, "templates")],
            ...
       }
   ]
   #设置数据库
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'db_ttsx',
           'HOST': '127.0.0.1',
           'PORT': '3306',
           'USER': 'root',
           'PASSWORD': '123456',
       }
   }
   
   #设置语言，地区
   LANGUAGE_CODE = 'zh-hans'
   TIME_ZONE = 'Asia/Chongqing'
   
   #设置static file dirctory
   STATIC_URL = '/static/'
   STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]
   ```

4. 添加templates和static 文件夹

   ```
   (venv) [ms@localhost ttsx_exercide]$ mkdir static
   (venv) [ms@localhost ttsx_exercide]$ mkdir templates
   ========================================================
   mkdir static
   mkdir templates
   ```

5. 更改ttsx_exercide/\__init__.py,加上

   ```
   import pymysql
   pymysql.install_as_MySQLdb()
   ```

6. 测试配置是否正确

   ```
   (new_venv) [ms@localhost new_project]$ python manage.py runserver
   Performing system checks...
   
   System check identified no issues (0 silenced).
   December 17, 2019 - 20:59:46
   Django version 2.1.8, using settings 'new_project.settings'
   Starting development server at http://127.0.0.1:8000/
   Quit the server with CONTROL-C.
   ```

   