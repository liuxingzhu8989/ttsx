from django.db import models
from db.models import BaseModels
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(BaseModels, AbstractUser):
    '''用户模型类
    '''
    class Meta:
        db_table = '用户表'
        verbose_name = '用户'
        verbose_name_plural = '用户'
