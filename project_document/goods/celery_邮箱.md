1. 安装celery

   ```
   (venv) [ms@localhost ttsx_exercide]$ pip install celery
   (venv) [ms@localhost ttsx_exercide]$ pip install itsdangerous
   ```

2. 163设置smtp server

   163账号，登录，设置，pop3/smtp服务，客户端授权密码

3. 配置settings.py

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi ttsx_exercide/settings.py
   ```

   #settings.py

   ```
   # 163 SMTP 配置
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'smtp.163.com'  # 网易 smtp 服务器地址
   EMAIL_PORT = 25  # 端口号
   #发送邮件的邮箱
   EMAIL_HOST_USER = 'maoshuai_work@163.com'
   #在邮箱中设置的客户端授权密码
   EMAIL_HOST_PASSWORD = 'maoshuai123456'
   #收件人看到的发件人
   EMAIL_FROM = 'ttsx<maoshuai_work@163.com>'
   ```

4. 添加celery文件

   ```
   (venv) [ms@localhost ttsx_exercide]$ mkdir celery_tasks
   (venv) [ms@localhost ttsx_exercide]$ touch celery_tasks/__init__.py
   (venv) [ms@localhost ttsx_exercide]$ vi celery_tasks/tasks.py
   ```

   #tasks.py

   ```
   from django.core.mail import send_mail
   from django.conf import settings
   from celery import Celery
   
   #设置django环境, 先设置，然后再导入models
   import os
   import django
   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ttsx_exercide.settings')
   django.setup()
   
   app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/1')
   
   @app.task
   def send_email_to_verify(email, username, token):
       subject='ttsx'
       message=''
       sender = settings.EMAIL_FROM
       receiver = [email]
       html_message = '<h1>%s</h1><a href="http://127.0.0.1:9001/user/active/%s">http://127.0.0.1/user/active/%s</a>'%(username,token,token)
   
       send_mail(subject, message, sender, receiver, html_message=html_message)
   
   ```

5. 在urls里面加re_path

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi apps/user/urls.py
   ```

   #urls.py

   ```
   from django.urls import path, re_path #add re_path
   from user.views import RegisterView, LoginView, LogOutView, InfoView, OrderView, SiteView, ActiveView #add ActiveView
   
   app_name = 'user'
   urlpatterns = [
       path('register/', RegisterView.as_view(), name = 'register'),
       path('login/', LoginView.as_view(), name = 'login'),
       path('logout/', LogOutView.as_view(), name = 'logout'),
       path('info/', InfoView.as_view(), name = 'info'),  #add info
       path('order/', OrderView.as_view(), name = 'order'), #add order
       path('site/', SiteView.as_view(), name = 'site'), #add site
       re_path('active/(?P<token>.*)$', ActiveView.as_view(), name='active'), #add re_path
   ]
   ```

6. 处理链接,在views里面定义

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi apps/user/views.py
   ```

   #views.py

   ```
   #序列化，加密
   from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
   from celery_tasks.tasks import send_email_to_verify
   from django.conf import settings
   
   #LoginView的post函数中
           if not user:
               user = User.objects.create_user(username, email, password)
               user.is_active = 0 #add this
               user.save()
           
           #add below, 加密user id
           serialize = Serializer(settings.SECRET_KEY)
           confirm = {'confirm':user.id}
           token = serialize.dumps(confirm) 
           token = token.decode()
           
           send_email_to_verify.delay(email, username, token) #add this
           ...
           
   
   class ActiveView(View):
          '''activate user
          '''
          def get(self, request, token):
              '''用户激活
              '''
              serializer = Serializer(settings.SECRET_KEY, 3600)
              try:
                  data = serializer.loads(token)
              except SignatuureExpired as e:
                  return HttpResponse('过期')
                  
          user_id = data['confirm']
          user = User.objects.get(id=user_id)
          user.is_active = 1
          user.save()
          return render(request, 'login.html')
   ```

7. 复制一份celery虚拟环境

   ```
   [ms@localhost Documents]$ mkdir celery_venv
   [ms@localhost Documents]$ cd celery_venv/
   [ms@localhost celery_venv]$ ls
   [ms@localhost celery_venv]$ cp -r ../venv/ .
   [ms@localhost celery_venv]$ vi venv/bin/activate
   ```

   #activate

   ```
   VIRTUAL_ENV="/home/ms/Documents/celery_venv/venv"#修改
   ```

8. 复制一份django项目到celery环境中

   ```
   (venv) [ms@localhost celery_venv]$ cp -r ../ttsx/ttsx/ttsx_exercide/ .
   ```

9. 激活celery虚拟环境

   ```
   [ms@localhost celery_venv]$ source venv/bin/activate
   ```

10. 开启celery

    ```
    (venv) [ms@localhost celery_venv]$ cd ttsx_exercide/
    (venv) [ms@localhost celery_venv]$ celery -A celery_tasks.tasks worker -l info
    ```

11. 测试

    注册用户，收到邮件，点击激活

