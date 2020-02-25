#coding=utf-8

from .default import *

#声明ORM底层所用数据库的访问URI
SQLALCHEMY_DATABASE_URI = 'mysql://root:1@127.0.0.1:3306/{database}'.format(database=PROJECT_NAME)
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False # we want to see sqlalchemy output
SQLALCHEMY_COMMIT_ON_TEARDOWN = True #当关闭数据库连接时是否自动提交事务

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = '123456'

# celery task
CELERY_BROKER_URL = 'redis://:{}@{}:{}/1'.format(REDIS_PASSWORD, REDIS_HOST, REDIS_PORT)
CELERY_RESULT_BACKEND = 'redis://:{}@{}:{}/1'.format(REDIS_PASSWORD, REDIS_HOST, REDIS_PORT)