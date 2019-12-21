1. 创建basemodel,加入create time, update time, delete time

   创建文件

   ```
   (new_venv) [ms@localhost new_project]$ mkdir base_model
   (new_venv) [ms@localhost new_project]$ touch base_model/__init__.py
   (new_venv) [ms@localhost new_project]$ vi base_model/models.py
   ```

   修改models文件

   ```
   from django.db import models
   
   class BaseModel(models.Model):
       create_time = models.DateTimeField(auto_now_add = True)
       update_time = models.DateTimeField(auto_now = True)
       is_delete = models.BooleanField(default = False)
   
       class Meta:
           abstract = True
   ```

2. 修改apps/user/models.py,加入

   ```
   #导入自定义类
   from base_model.models import BaseModel
   
   #继承django User
   from django.contrib.auth.models import AbstractUser
   
   
   class User(BaseModel, AbstractUser):
       '''
           自定义用户类
       '''
       class Meta:
           db_table = 'user_table'
           verbose_name = 'user_v'
           verbose_name_plural = 'user_p'
   ```

3. 修改new_project/settings.py,加入

   ```
   #apps/user/apps.py下有name=user, 自动导入app下models
   AUTH_USER_MODEL = 'user.User'
   ```

4. 数据库操作

   创建database

   ```
   (new_venv) [ms@localhost new_project]$ mysql -u root -p
   
   mysql> show databases;
   mysql> create database db_ttsx default charset utf8;
   ```

   生成数据迁移文件，orm生成table

   ```
   (new_venv) [ms@localhost new_project]$ python manage.py makemigrations
   (new_venv) [ms@localhost new_project]$ python manage.py migrate
   ```

5. admin管理用户

   创建超级用户

   ```
   (new_venv) [ms@localhost new_project]$ python manage.py createsuperuser
   ```

   将user加入到admin

   ```
   [ms@localhost new_project]$ vi apps/user/admin.py 
   
   #code
   from user.models import User
   
   admin.site.register(User)
   ```

6. 测试

   启动server

   ```
   (new_venv) [ms@localhost new_project]$ python manage.py runserver
   ```

   web访问admin

   ```
   http://127.0.0.1:8000/admin/
   ```

   GUI可编辑用户





