1. 安装

   ```
   pip install celery
   ```

2. project下建立celery_task包文件夹

3. 建立tasks.py

   ```
   from celery import Celery
   
   #创建celery实例对象
   app = Celery('celery_tasks.tasks',broker='redis://ip:port/database')
   
   #定义任务函数
   @app.task
   def send_register_active_email(to_email, username, token):
   	'''发送激活邮件
   	'''
   	#组织邮件信息
   ```

4. 在views.py里面调用send_register_active_email

   ```
   send_register_active_email.delay(email, username, token)
   ```

5. django项目复制到worker

6. 启动worker

   ```
   celery -A celery_tasks.tasks worker -l info
   ```

7. 如果需要用到django配置文件，导入django初始化，复制wsgi.py相关内容，在处理端tasks.py

   ```
   import os
   import django
   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ddfresh.settings')
   django.setup()
   ```

   