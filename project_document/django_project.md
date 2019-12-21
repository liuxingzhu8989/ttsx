1. 生成project项目

   ```
   (new_venv) [ms@localhost new_project]$ django-admin startproject new_project .
   ```

2. 生成app

   ```
   #创建目录
   (new_venv) [ms@localhost new_project]$ mkdir apps
   
   #创建user, goods, order, cart
   (new_venv) [ms@localhost new_project]$ mkdir apps/user
   (new_venv) [ms@localhost new_project]$ mkdir apps/goods
   (new_venv) [ms@localhost new_project]$ mkdir apps/order
   (new_venv) [ms@localhost new_project]$ mkdir apps/cart
   ```

3. 更改new_project/settings.py

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
   #STATIC_URL = '/static/'
   STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]
   ```

4. 添加templates和static 文件夹

   ```
   (new_venv) [ms@localhost new_project]$ mkdir static
   (new_venv) [ms@localhost new_project]$ mkdir templates
   ```

5. 更改new_project/\__init__.py,加上

   ```
   import pymysql
   pymysql.Install_as_MySQLdb()
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

   