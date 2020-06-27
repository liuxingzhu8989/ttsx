1. git配置

   配置git账号

   ```
   [ms@localhost new_project]$  
   [ms@localhost new_project]$ git config --global user.email "liuxingzhu8989@163.com"
   ```

   查看git配置

   ```
   [ms@localhost new_project]$ git config --list
   user.name=liuxingzhu898
   user.email=liuxingzhu8989@163.com
   push.default=simple
   core.repositoryformatversion=0
   core.filemode=true
   core.bare=false
   core.logallrefupdates=true
   remote.origin.url=git@github.com:liuxingzhu8989/ttsx.git
   remote.origin.fetch=+refs/heads/*:refs/remotes/origin/*
   branch.master.remote=origin
   branch.master.merge=refs/heads/master
   ```

2. python安装

   安装依赖库

   ```
   yum -y install wget gcc zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel libffi-devel
   ```

   安装python3

   ```
   # python包
   wget https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tgz
   
   #解压
   tar -xvf Python-3.7.3.tar
   
   #进入目录
   cd Python-3.7.3
   
   #安装
   ./configure --prefix=/usr/local/python37 --enable-optimizations
   sudo make && make install
   ```

   修改.bash_profile,加入PATH

   ```
   #修改bash文件
   vim .bash_profile
   
   #export path
   export PATH=$PATH:/usr/local/python37/bin
   
   #激活
   source ~/.bash_profile
   ```

3. 虚拟环境

   创建环境

   ```
   [ms@localhost ttsx]$ python -m venv venv_name
   ```

   激活虚拟环境

   ```
   [ms@localhost ttsx]$ source venv/bin/activate
   ```

   #退出虚拟机环境

   ```
   (venv) [ms@localhost ttsx]$ deactive
   ```

4. 安装django相关包

   升级

   ```
   pip3 install --upgrade pip
   ```

   安装django

   ```
   pip3 install django==2.1.8
   ```

   <hr>

[解决超时问题](https://blog.csdn.net/wukai0909/article/details/62427437)

#修改~/.pip/pip.conf

   #~/.pip/pip.conf


   ```
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
[install]
trusted-host=mirrors.aliyun.com
   ```

   #其他相关命令

   查看包

   ```
   pip show --file package-name
   ```

   升级包

   ```
   pip install --upgrade package-name
   ```

   卸载包

   ```
   pip uninstall package-name
   ```

   待更新包

   ```
   pip list --outdate         
   ```

5. mysql安装 #TODO

   安装pymysql

   ```
   (venv) [ms@localhost ttsx_exercide]$ pip3 install pymysql
   ```

6. 安装redis

   ```
   (venv) [ms@localhost ttsx_exercide]$ sudo yum -y install redis
   ```

   启动

   ```
   (venv) [ms@localhost ttsx_exercide]$ redis-server &
   ```

   检查

   ```
   (venv) [ms@localhost ttsx_exercide]$ redis-cli 
   127.0.0.1:6379> 
   ```

   

