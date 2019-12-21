from django.db import models

class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add = True)
    update_time = models.DateTimeField(auto_now = True)
    is_delete = models.BooleanField(default = False)

    class Meta:
        abstract = True
