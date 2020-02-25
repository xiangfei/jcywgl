#coding=utf-8

from .default import *

DEBUG = False
TESTING = False

SQLALCHEMY_DATABASE_URI = 'mysql://root:averystrongpasswordotherwise@10.0.34.201:3306/{database}'.format(database=PROJECT_NAME)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False 
SQLALCHEMY_COMMIT_ON_TEARDOWN = True 


REDIS_HOST = '10.0.34.201'
REDIS_PORT = 6379
REDIS_PASSWD = ''

# celery task
CELERY_BROKER_URL = 'redis://:{0}@{1}:{2}/1'.format(REDIS_PASSWD, REDIS_HOST, REDIS_PORT)
CELERY_RESULT_BACKEND = 'redis://:{0}@{1}:{2}/1'.format(REDIS_PASSWD, REDIS_HOST, REDIS_PORT)
CELERY_TIMEZONE = 'Asia/Shanghai'