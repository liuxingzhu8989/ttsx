from django.db import models

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
