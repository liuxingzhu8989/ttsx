1. install

   ```
   pip install django-debug-toolbar==1.11
   ```

2. configure settings.py

   ```
   INSTALLED_APPS = [
   	...
   	debug_toolbar,
   ]
   
   MIDDLEWARE = [
   ...
   	'debug_toolbar.middleware.DebugToolbarMiddleware',
   ]
   
   DEBUG_TOOLBAR_CONFIG = {
       'JQUERY_URL': 'https://cdn.bootcss.com/jquery/3.3.1/jquery.min.js',
       'SHOW_COLLAPSED':True,
       'SHOW_TOOLBAR_CALLBACK': lambda x:True,
   }
   ```

3. configure project urls.py

   ```
   from django.conf import settings
   if settings.DEBUG:
       import debug_toolbar
       urlpatterns.insert(0, path('__debug__/', include(debug_toolbar.urls)))
   ```

   

