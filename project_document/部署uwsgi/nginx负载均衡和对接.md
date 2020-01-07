1. 对接

   对外的ngnix需要将请求传到静态页面的nginx,以获取静态页面。更改对外的nginx.conf，在监听端口加上

   ```
   location = / {
   	proxy_pass http://ip:port;
   }
   ```

   重启nginx

2. 负载均衡

   copy一份uwsgi.ini，更改文件的端口号，pid， log， 启动

   修改nginx配置文件

   ```
   upstream ttsx {
   	server 127.0.0.1:8000;
   	server 127.0.0.1:8001;
   }
   
   location / {
       include uwsgi_params;
       uwsgi_pass ttsx;
   }
   ```

   重启nginx，分别查看uwsgi.log测试是否实现了负载均衡

