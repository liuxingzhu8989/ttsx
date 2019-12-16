from django.db import models
from db.models import BaseModel
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(BaseModel, AbstractUser):
    '''用户模型类
    '''
    class Meta:
        db_table = '用户表'
        verbose_name = '用户'
        verbose_name_plural = '用户'

class AddressManager(models.Manager):
    def get_default_address(self, user):
        try:
            address = self.get(user=user, is_default=True)
        except self.model.DoesNotExist:
            address = None

        return address
    
class Address(BaseModel):
    user = models.ForeignKey('User', verbose_name='用户', on_delete='CASCADE')
    receiver = models.CharField(max_length=100)
    addr = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=6)
    phone = models.CharField(max_length=11)
    is_default = models.BooleanField(default=False)
    
    objects = AddressManager()
    class Meta:
        db_table = '地址表'
