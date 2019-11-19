### 用户

>django自带认证系统

```
from django.conrtib.auth.models import AbstractUser
class User(AbstractUser)：
	class Meta:
		db_table='用户'
		verbose_name='用户表'
```



### 收件地址表

```
user = models.ForeignKey(User, verbose_name="用户账户")
zip_code = models.CharField(max_length=10, verbose_name="邮编")
is_defualt = models.BooleanField(default=False, verbose_name="是否默认")
```

### 商品表

```
首页商品类别logo:logo = models.Charfield()
image = models.imageFiled(upload_to='type', verbose_name="商品类别")
```

### 商品sku表

```
detail = HTMLField(blank=True, verbose_name='商品详情')
status_choice=(（0，’下线‘），（1，’上线‘）)
status = models.SmallIntergerField(default = 1,choices =status_choice)
```

### 轮播表

```
url = models.URLField(verbose_name='活动链接')
```

### 订单表

```
order_id = models.CharField(primary_key=True)
```

### 基础模型

```
class BaseModel(models.Model):
	create_time = models.DateTimeField(auto_now_add=True)
	update_time = models.DateTimeField(auto_now=True)
	is_delete=models.BooleanField()
	class Meta:
		#标记为抽象类
		abstract = True
```

类属性：

```
class User:
	class Meta:
		db_table = 'table_name'
		verbose_name = 'user'
		verbose_name_plural = verbose_name
```

