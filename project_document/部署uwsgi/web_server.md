1. 安装uwsig

   安装软件

   ```
   (venv) [ms@localhost ttsx]$ pip install uwsgi
   ```

   修改settings配置文件

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi ttsx_exercide/settings.py 
   ```

   #settings.py

   ```
   DEBUG = False
   
   ALLOWED_HOSTS = ['*']
   ```

2. 添加uwsgi配置文件

   ```
   (venv) [ms@localhost ttsx_exercide]$ cd ttsx_exercide/
   (venv) [ms@localhost ttsx_exercide]$ vi uwsgi.ini
   ```

   #uwsgi.ini

   ```
   [uwgi]
   #使用nginx连接时使用
   #socket=127.0.0.1:8080
   #直接做web服务器使用
   http=127.0.0.1:8000
   #项目目录
   chdir=/home/ms/Documents/ttsx/ttsx/ttsx_exercide
   #项目中wsgi.py文件的目录，相对于项目目录
   wsgi-file=ttsx_exercide/wsgi.py
   processes=4
   #指定工作进程的线程数
   threads=2
   master=True
   #主进程
   pidfile=uwsgi.pid
   #uwsgi log
   daemonize=uwsgi.log
   virtualenv=/home/ms/Documents/venv
   ```

3. 启动与停止

   启动

   ```
   (venv) [ms@localhost ttsx_exercide]$ uwsgi --ini uwsgi.ini 
   ```

   查看

   ```
   (venv) [ms@localhost ttsx_exercide]$ ps -ef|grep uwsgi
   ms        1140     1 13 10:15 ?        00:00:00 uwsgi --ini uwsgi.ini
   ms        1150  1140  0 10:15 ?        00:00:00 uwsgi --ini uwsgi.ini
   ms        1151  1140  0 10:15 ?        00:00:00 uwsgi --ini uwsgi.ini
   ms        1153  1140  0 10:15 ?        00:00:00 uwsgi --ini uwsgi.ini
   ms        1154  1140  0 10:15 ?        00:00:00 uwsgi --ini uwsgi.ini
   ms        1158  1140  0 10:15 ?        00:00:00 uwsgi --ini uwsgi.ini
   ms        1242 17471  0 10:15 pts/2    00:00:00 grep --color=auto uwsgi
   ```

   停止

   ```
   (venv) [ms@localhost ttsx_exercide]$ uwsgi --stop uwsgi.pid 
   ```

   查看

   ```
   (venv) [ms@localhost ttsx_exercide]$ ps -ef|grep uwsgi
   ms        2114 17471  0 10:16 pts/2    00:00:00 grep --color=auto uwsgi
   ```

   