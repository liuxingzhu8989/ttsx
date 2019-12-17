1. 创建basemodel,加入create time, update time, delete time

   ```
   (new_venv) [ms@localhost new_project]$ mkdir base_model
   (new_venv) [ms@localhost new_project]$ touch base_model/__init__.py
   (new_venv) [ms@localhost new_project]$ vi base_model/models.py
   
   #modify models文件
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
   #指定user模块类
   AUTH_USER_MODEL = 'user.User'
   ```

   