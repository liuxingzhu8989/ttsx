1. 安装

   ```
   (venv) [ms@localhost ttsx_exercide]$ pip install celery
   ```

2. 新建文件

   ```
   (venv) [ms@localhost ttsx_exercide]$ mkdir celery_tasks
   (venv) [ms@localhost ttsx_exercide]$ touch celery_tasks/tasks.py
   (venv) [ms@localhost ttsx_exercide]$ touch celery_tasks/__init__.py
   ```

3. 编辑tasks.py

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi celery_tasks/tasks.py
   ```

   #tasks.py

   ```
   #Celery类
   from celery import Celery
   
   #django配置
   from django.conf import settings
   
   import os
   import django
   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ddfresh.settings')
   django.setup()
   
   #redis数据库
   from goods.models import GoodsType, IndexGoodsBanner, IndexTypeGoodsBanner,IndexPromotionBanner
   app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/1')
   
   #生成静态页面
   @app.task
   def generate_index_page():
       types = GoodsType.objects.all()
       goods_banners = IndexGoodsBanner.objects.all()
       type_goods_banners = IndexTypeGoodsBanner.objects.all().order_by('index')
       promotion_banners = IndexPromotionBanner.objects.all().order_by('index')
   
       context = {'types':types,
                   'goods_banners': goods_banners,
                   'type_goods_banners': type_goods_banners,
                   'promotion_banners':promotion_banners,
                 }
   
       temp = loader.get_template('static_index.html')
       index_static = temp.render(context)
       
       save_path = os.path.join(settings.BASE_DIR, 'static/index.html')    
       with open(save_path, "w") as f:
           f.write(index_static)
   ```

   