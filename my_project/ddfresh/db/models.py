from django.db import models

class BaseModels(models.Model):
    create_time = models.DateTimeField(auto_now_add = True, verbose_name =' 添加时间')
    update_time = models.DateTimeField(auto_now = True, verbose_name = '更新时间')
    is_delete = models.BooleanField(default = False)

    class Meta:
        abstract = True