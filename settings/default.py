# coding=utf-8

import os
import socket
import pymysql

from datetime import timedelta

pymysql.install_as_MySQLdb()


# dev server
DEV_SERVER_IP_LIST = ['10.0.34.48']
# test server
TEST_SERVER_IP_LIST = []
# pre server
PRE_SERVER_IP_LIST = []
# online server
PRODUCT_SERVER_IP_LIST = ['10.0.34.201']

# 自动创建文件夹
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAR_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir))

LOG_DIR = os.path.join(PAR_DIR, 'var', 'logs')
TMP_DIR = os.path.join(PAR_DIR, 'var', 'tmp')
DOWN_DIR = os.path.join(PAR_DIR, 'downloads')
try:
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    if not os.path.exists(TMP_DIR):
        os.makedirs(TMP_DIR)
    if not os.path.exists(DOWN_DIR):
        os.makedirs(DOWN_DIR)
except:
    pass


# 项目名称
PROJECT_NAME = 'jcywgl'


# URLS
URLS = [
    {'view': 'apps.account.views.accountRouter', 'url_prefix':'/v1.0/account'},
    {'view': 'apps.resource.frameworkRouter', 'url_prefix':'/v1.0/framework'},
    {'view': 'apps.resource.projectRouter', 'url_prefix':'/v1.0/project'},
    {'view': 'apps.resource.moduleRouter', 'url_prefix':'/v1.0/module'},
]


# extensions
EXTENSIONS = [
    'extra.basic.db',
    'extra.basic.migrate',
    'extra.basic.celery',
    'extra.basic_redis.myredis',
    'extra.basic_ldap.myldap'
    #'extra.basic_gitlab.mygitlab'
]


# security
SECRET_KEY = 'n-2)5evd4&%7im5-3_ae(ushagr*0ktrhp97ob$b3-^r5-9xdh'
SESSION_COOKIE_NAME = 'AUID'
PERMANENT_SESSION_LIFETIME = 3600
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_DOMAIN = ''


# env_debug_test
DEBUG = True
TESTING = True


# ldap configure
LDAP_URI = '10.0.28.10'
LDAP_PORT = 389
LDAP_BASE_DN = 'dc=gold-finance,dc=local'
LDAP_USER = "ittest"
LDAP_PASSWD = "2345.com"


# gitlab configure
GITLAB_URI = 'http://git.jc'
GITLAB_PRIVATE_TOKEN = 'fFZjxzWn-osXh3PHzRBs'


# logger
ERROR_LOG_LIMIT = 200000
LOG_PATH = os.path.join(LOG_DIR, 'default.log')


# celery task
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_IMPORTS = ('apps.tasks.syncldap', )
CELERYBEAT_SCHEDULE = {
    # 定义任务名称：import_data
    # 执行规则：每10秒运行一次
    'user_ldap': {
        'task': 'apps.tasks.syncldap.user_ldap',
        'schedule': timedelta(seconds=10*60)
    },
}


try:
    hostname = socket.gethostname()
except Exception as e:
    hostname = ''

# MySQL - mysql://username:password@hostname/database
# Postgre - postgresql://username:password@hostname/database
# SQLite - sqlite:////absolute/path/to/database
if hostname == 'WangJunhuis-MacBook-Pro-2.local' or hostname == 'localhost':
    #声明ORM底层所用数据库的访问URI
    SQLALCHEMY_DATABASE_URI = 'mysql://root:1@127.0.0.1:3306/{database}'.format(database=PROJECT_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = False # we want to see sqlalchemy output
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True #当关闭数据库连接时是否自动提交事务

    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_PASSWORD = ''

    # celery task
    CELERY_BROKER_URL = 'redis://:{}@{}:{}/1'.format(REDIS_PASSWORD, REDIS_HOST, REDIS_PORT)
    CELERY_RESULT_BACKEND = 'redis://:{}@{}:{}/1'.format(REDIS_PASSWORD, REDIS_HOST, REDIS_PORT)


elif hostname == '你本地的hostname':
    pass
