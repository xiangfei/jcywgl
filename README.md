
> init env

```
1.install mysql redis

2.install pip
yum install epel-release
yum install python-pip

3.install python3
yum install zlib-devel bzip2-devel openssl-devel ncurese-devel

wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tar.xz

 cd Python-version
 ./configure --prefix=/usr/local/python3
 make && make install

ln -s /usr/local/python3/bin/python3.5 /usr/bin/python
ln -s /usr/local/python3/bin/pip3 /usr/bin/pip

4.install api venv
pip install virtualenv
virtualenv -p python3 venv

source venv/bin/activate

pip install -r requirements.txt
```

> start project

```
source venv/bin/activate

1.修改指定配置mysql,redis

2.初始化数据库
python manage.py db init

python manage.py db migrate

python manage.py db upgrade

3.启动
python run_server.py all

```

> 项目结构

```
jcywgl
    -apps 应用目录
    -downloads 下载目录
    -extra 引入第三方模块
    -migrations sqlalchemy自动生成
    -script 脚本
    -settings 项目配置文件
    -utils 工具类
    -var 日志、进程文件
    -web vuejs项目
    -venv 虚拟环境 
```

> Celery的使用

```
// 启动
celery -A startup.celery worker --loglevel=info

// 启动心跳，执行定时任务
celery -A startup.celery worker -l INFO -c 100 -B
```