1. 安装

   ```
   (venv) [ms@localhost ttsx_exercide]$ pip install django-tinymce==2.6.0
   ```

2. 修改settings.py

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi ttsx_exercide/settings.py 
   ```

   #settings.py

   ```
   INSTALLED_APPS = [
       ...
       'user',
       'goods',
       'cart',
       'order',
       'tinymce',  #add the line
   ]
   
   TINYMCE_DEFAULT_CONFIG = {
   	'theme': 'advanced',
   	'width': 600,
   	'height': 400,
   }
   ```

3. 修改urls.py

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi ttsx_exercide/urls.py 
   ```

   #urls.py

   ```
   urlpatterns = [
       path('admin/', admin.site.urls),
       path('tinymce/', include('tinymce.urls')), #add the line
       path('user/', include('user.urls'), name = 'user'),
       path('goods/', include('goods.urls'), name = 'goods'),
   ]
   ```

4. 测试

   修改models.py
   
   ```
from tinymce.models import HTMLField
   detail = HTMLField(verbose_name='商品详情')
   ```
   
   