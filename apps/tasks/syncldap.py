#coding=utf-8
import os
from extra.basic import celery

# 定时导入LDAP用户数据
@celery.task
def user_ldap():
    result = os.system('python {0}/manage.py ldap'.format(os.getcwd()))
    print(result)

# 定时导入
@celery.task
def import_data():
    print("定时任务：每10秒执行一次")