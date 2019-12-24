1. 修改uwsgi.ini文件

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi uwsgi.ini 
   ```

   #uwsgi.ini

   ```
   [uwsgi]
   #使用nginx连接时使用
   socket=127.0.0.1:8000
   #直接做web服务器使用
   #http=127.0.0.1:8000
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

2. 修改nginx配置文件

   ```
   (venv) [ms@localhost ttsx_exercide]$ sudo vi /usr/local/nginx/conf/nginx.conf
   ```

   #nginx.conf

   ```
   		location / {
               include uwsgi_params;
               uwsgi_pass 127.0.0.1:8000;
           }
   ```

3. 启动nginx

   ```
   (venv) [ms@localhost sbin]$ sudo ./nginx
   #重启
   (venv) [ms@localhost sbin]$ sudo ./nginx -s reload
   ```

   查看

   ```
   (venv) [ms@localhost sbin]$ ps -ef|grep nginx
   root      1024     1  0 Dec22 ?        00:00:00 nginx: master process /usr/local/nginx/sbin/nginx
   root     12611  1024  0 10:25 ?        00:00:00 nginx: worker process
   ms       13228 24712  0 10:25 pts/3    00:00:00 grep --color=auto nginx
   ```

4. 启动uwsgi

   ```
   (venv) [ms@localhost ttsx_exercide]$ uwsgi --ini uwsgi.ini 
   ```

5. web登录页面查看