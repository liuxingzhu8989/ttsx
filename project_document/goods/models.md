1. ImageField安装pillow

   ```
   (venv) [ms@localhost ttsx_exercide]$ pip install Pillow
   ```

2. 模型

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi apps/goods/models.py 
   ```

   #models.py

   ```
   from django.db import models
   from base_model.models import BaseModel
   from tinymce.models import HTMLField
   
   class GoodsType(BaseModel):
       '''商品类型'''
       name = models.CharField(max_length=20)
       logo = models.CharField(max_length=20)
       image = models.ImageField(upload_to='type')
   
       class Meta:
           db_table = 'df_goods_type'
           verbose_name = 'good_type_v'
           verbose_name_plural = 'good_type_p'
   
       def __str__(self):
           return str(self.name)
   
   
   class GoodsSKU(BaseModel):
       '''商品SKU'''
       status_choices = (
           (0, '下线'),
           (1, '上线'),
       )
       type = models.ForeignKey('GoodsType', on_delete='CASCADE')
       goods = models.ForeignKey('Goods', on_delete='CASCADE')
       name = models.CharField(max_length=20)
       desc = models.CharField(max_length=256)
       price = models.DecimalField(max_digits=10, decimal_places=2)
       unite = models.CharField(max_length=20)
       image = models.ImageField(upload_to='goods')
       stock = models.IntegerField(default=1)
       sales = models.IntegerField(default=0)
       status = models.SmallIntegerField(default=1, choices=status_choices)
   
       def __str__(self):
           return str(self.name)
   
       class Meta:
           db_table = 'df_goods_sku'
           verbose_name = 'goods_sku_v'
           verbose_name_plural = 'goods_sku_p'
   
   
   class Goods(BaseModel):
       '''商品SPU'''
       name = models.CharField(max_length=20)
       # 富文本类型:带有格式的文本
       detail = HTMLField(blank=True)
   
       def __str__(self):
           return str(self.name)
   
       class Meta:
           db_table = 'df_goods'
           verbose_name = 'goods_v'
           verbose_name_plural = 'goods_p'
   
   
   class GoodsImage(BaseModel):
       '''商品图片'''
       sku = models.ForeignKey('GoodsSKU', on_delete='CASCADE')
       image = models.ImageField(upload_to='goods')
   
       class Meta:
           db_table = 'df_goods_image'
           verbose_name = 'goods_image_v'
           verbose_name_plural = 'goods_image_p'
   
   
   class IndexGoodsBanner(BaseModel):
       '''首页轮播商品展示'''
       sku = models.ForeignKey('GoodsSKU', on_delete='CASCADE')
       image = models.ImageField(upload_to='banner')
       index = models.SmallIntegerField(default=0) # 0 1 2 3
   
       def __str__(self):
           return str(self.sku)
   
       class Meta:
           db_table = 'df_index_banner'
           verbose_name = 'index_goods_banner_v'
           verbose_name_plural = 'index_goods_banner_p'
   
   
   class IndexTypeGoodsBanner(BaseModel):
       '''首页分类商品展示'''
       DISPLAY_TYPE_CHOICES = (
           (0, "标题"),
           (1, "图片")
       )
   
       type = models.ForeignKey('GoodsType', on_delete='CASCADE')
       sku = models.ForeignKey('GoodsSKU', on_delete='CASCADE')
       display_type = models.SmallIntegerField(default=0, choices=DISPLAY_TYPE_CHOICES)
       index = models.SmallIntegerField(default=0)
   
       def __str__(self):
           return str(self.type) + "_" + str(self.sku) + "_" + str(self.DISPLAY_TYPE_CHOICES[self.display_type][1])
   
       class Meta:
           db_table = 'df_index_type_goods'
           verbose_name = "index_type_goods_v"
           verbose_name_plural = 'index_type_goods_p'
   
   class IndexPromotionBanner(BaseModel):
       '''首页促销活动'''
       name = models.CharField(max_length=20)
       url = models.CharField(max_length=256)
       image = models.ImageField(upload_to='banner')
       index = models.SmallIntegerField(default=0)
   
       def __str__(self):
           return str(self.name)
   
       class Meta:
           db_table = 'df_index_promotion'
           verbose_name = "index_promotion_v"
           verbose_name_plural = 'index_promotion_p'
   ```

3. 生成table

   ```
   (venv) [ms@localhost ttsx_exercide]$ python manage.py makemigrations
   (venv) [ms@localhost ttsx_exercide]$ python manage.py migrate
   ```

4. 将goods加入admin

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi apps/goods/admin.py
   ```

   #admin.py

   ```
   from django.contrib import admin
   from goods.models import Goods,GoodsType,IndexPromotionBanner,IndexGoodsBanner,IndexTypeGoodsBanner
   
   admin.site.register(Goods)
   admin.site.register(GoodsType)
   admin.site.register(IndexGoodsBanner)
   admin.site.register(IndexTypeGoodsBanner)
   admin.site.register(IndexPromotionBanner)
   ```

5. 测试

   创建admin超级用户

   ```
   (venv) [ms@localhost ttsx_exercide]$ python manage.py createsuperuser
   ```

   新建用户名和密码用于进入admin管理
   
   web浏览器输入
   
   ```
   http://127.0.0.1:9001/admin
   ```
   
   出现错误
   
   >/home/ms/Documents/venv/lib/python3.7/site-packages/django/forms/boundfield.py in as_widget, line 93
   
   直接注释掉第93行
   
   ```
   (venv) [ms@localhost ttsx_exercide]$ vi /home/ms/Documents/venv/lib/python3.7/site-packages/django/forms/boundfield.py +93
   ```
   
   #boundfield.py
   
   ```
   #renderer=self.form.renderer, #comment
   ```
   
6. 将index需要的图片加入数据库

