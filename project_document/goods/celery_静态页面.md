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

   