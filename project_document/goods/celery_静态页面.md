1. 修改tasks.py

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi celery_tasks/tasks.py
   ```

   #tasks.py

   ```
   #静态页面
   from django.template import loader, RequestContext
   
   @app.task
   def generate_static_index():
           types = GoodsType.objects.all()
           # 获取首页轮播商品信息
           goods_banners = IndexGoodsBanner.objects.all()
           # 获取首页促销活动信息
           promotion_banners = IndexPromotionBanner.objects.all().order_by('index')
   
           for type in types: # GoodsType
                   # 获取type种类首页分类商品的图片展示信息
                   image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by('index')
                   # 获取type种类首页分类商品的文字展示信息
                   title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by('index')
   
                   # 动态给type增加属性，分别保存首页分类商品的图片展示信息和文字展示信息
                   type.image_banners = image_banners
                   type.title_banners = title_banners
   
           context = {'types': types,
                      'goods_banners': goods_banners,
                      'promotion_banners': promotion_banners,}
                      
   		temp = loader.get_template('static_index.html')
   		static_index_html = temp.render(context)
           save_path = os.path.join(settings.BASE_DIR, 'static/index.html')
       with open(save_path, 'w') as f:
           f.write(static_index_html)
   ```

2. 测试

   ```
   (venv) [ms@localhost ttsx_exercide]$ python manage.py shell
   >>> from celery_tasks.tasks import generate_static_index
   >>> generate_static_index.delay()
   ```

   在celery里面会看到index.html页面

   ```
   (venv) [ms@localhost ttsx_exercide]$ pwd
   /home/ms/Documents/celery_venv/ttsx_exercide
   (venv) [ms@localhost ttsx_exercide]$ ls static/
   css  images  index.html  js
   ```

3. 设置nginx监听80端口，默认访问

   修改index路径

   ```
   (venv) [ms@localhost ttsx_exercide]$ sudo vi /usr/local/nginx/conf/nginx.conf
   ```

   #nginx.conf

   ```
   location / {
               root   /home/ms/Documents/celery_venv/ttsx_exercide/static;
               index  index.html index.htm;
           }  #配置为celery目录
   ```

   启动

   ```
   (venv) [ms@localhost ttsx_exercide]$ sudo /usr/local/nginx/sbin/nginx
   ```

   查看

   ```
   (venv) [ms@localhost ttsx_exercide]$ ps -ef|grep nginx
   root      9699     1  0 09:14 ?        00:00:00 nginx: master process /usr/local/nginx/sbin/nginx
   root      9700  9699  0 09:14 ?        00:00:00 nginx: worker process
   ms        9715  5338  0 09:15 pts/2    00:00:00 grep --color=auto nginx
   ```

4. admin更新静态页面

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi apps/goods/admin.py 
   ```

   #admin.py

   ```
   #celery 静态页面
   from celery_tasks.tasks import generate_static_index
   
   #类
   class IndexPromotionBannerAdmin(admin.ModelAdmin):
       def save_model(self, request, obj, form, change):
           super().save_model(request, obj, form, change)
           generate_static_index.delay()
   
       def delete_model(self, request, obj):
           super().delete_model(self, request, obj)
           generate_static_index.delay()
           
   #注册
   admin.site.register(IndexPromotionBanner, IndexPromotionBannerAdmin)
   ```

5. 测试

   打开admin站点，更改促销活动图片，观察首页是否刷新