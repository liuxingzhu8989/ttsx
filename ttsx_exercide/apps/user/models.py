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

class AddressManager(models.Manager):
    def get_default_address(self, user):
        try:
            address = self.model.objects.get(user=user, is_default = True)
        except self.model.DoesNotExist:
            address = None
        return address
    
class Address(BaseModel):
    user = models.ForeignKey('User', on_delete='CASCADE')
    receiver = models.CharField(max_length=20)
    addr = models.CharField(max_length=256)
    zip_code = models.CharField(max_length=6)
    phone_number = models.CharField(max_length=11)
    is_default = models.BooleanField(default = False)
    
    objects = AddressManager()

    class Meta:
        db_table = 'df_address'
        verbose_name = 'address_v'
        verbose_name_plural = 'user_p'
    
