> 用处：缓存服务器

>session服务器

>购物车模块



1. 安装

   >redis在centos里面是三方软件，先安装epel-release
   >
   >```
   >yum install epel-release
   >```
   >
   >查看
   >
   >```
   > yum repolist
   >```
   >
   >安装
   >
   >```
   >yum install redis
   >```
   >
   >启动
   >
   >```
   >systemctl start redis
   >```
   >
   >查看启动状态
   >
   >```
   >systemctl status redis
   >```