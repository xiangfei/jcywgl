#coding=utf-8

import os
import sys
import json

from flask_script import Command, Option, Manager, Server, commands
from flask_migrate import MigrateCommand

from settings import default
from app import create_app
from apps.account.models import User, Department
from apps.account.service import AccountService, DepartmentService
from extra.basic import db, celery
from extra.basic_ldap import myldap

app = create_app(default.PROJECT_NAME) 


class CreateDB(Command):
    """
    Create database
    """
    def run(self):
        try:
            db.create_all()
        except ImportError:
            print("Please, make sure db.create_all exists in order to create a db.")


class DropDB(Command):
    """
    Drop database
    """
    def run(self):
        try:
            db.drop_all()
        except ImportError:
            print("Please, make sure db.drop_all exists in order to drop a db.")


groups = 'OU=信息技术部,OU=正大道,OU=金诚集团,ou=gold-finance,dc=gold-finance,dc=local'
filter = '(objectclass=user)'
attributes = {
    'sAMAccountName':'username',
    'mail':'email',
    'mobile':'mobile',
    'cn':'chinese_name'
}

class SyncUserldap(Command):
    """
    Synchronize users and groups from an authoritative LDAP server
    """
    def run(self):
        # 默认邮件是唯一的
        flag, result = myldap.ldap_search(groups, filter, attributes.keys())
        if flag:
            dp_list = []
            for item in result:
                user = json.loads(item.entry_to_json())
                dn = user.get('dn')
                ou_list = dn.split(',OU=')
                if len(ou_list) == 6:
                    dp_list.append(ou_list[1])
                elif len(ou_list) == 7:
                    dp_list.append(ou_list[2])
                else:
                    pass
                params = {'ldap_dn':dn}
                for k, v in attributes.items():
                    params[v] = user.get('attributes').get(k)[0] if user.get('attributes').get(k) else None
                username=params.get('username')
                account = AccountService(username=username)
                if account.is_user_exist():
                    flag, user = account.update_user(params)
                    print('{0} is updated success'.format(username))
                else:
                    flag, user = AccountService.save_user(params)
                    print('{0} is saved success'.format(username))
            department = list(set(dp_list))
            deps = Department.query.with_entities(Department.department).all()
            for item in department:
                if (item,) not in deps:
                    flag, de = DepartmentService.save_depart(item)
                    print('{0} is saved success'.format(item))
        else:
            print("Please check, ldap is error")


class GunicornServer(Command):

    description = 'Run the app within Gunicorn'

    def __init__(self, host='127.0.0.1', port=9000, workers=4):
        self.port = port
        self.host = host
        self.workers = workers

    def get_options(self):
        return (
            Option('-H', '--host',
                   dest='host',
                   default=self.host),

            Option('-p', '--port',
                   dest='port',
                   type=int,
                   default=self.port),

            Option('-w', '--workers',
                   dest='workers',
                   type=int,
                   default=self.workers),
        )

    # With the latest version of Flask-Script, change the method handle with __call__. 
    # old flask-script vs new flask-script
    def __call__(self, app, host, port, workers):
        from gunicorn import version_info

        if version_info < (0, 9, 0):
            from gunicorn.arbiter import Arbiter
            from gunicorn.config import Config
            arbiter = Arbiter(Config({'bind': "%s:%d" % (host, int(port)),'workers': workers}), app)
            arbiter.run()
        else:
            from gunicorn.app.base import Application

            class FlaskApplication(Application):
                def init(self, parser, opts, args):
                    return {
                        'bind': '{0}:{1}'.format(host, port),
                        'workers': workers 
                    }

                def load(self):
                    return app

            FlaskApplication().run()


if __name__ == "__main__":

    manager = Manager(app)
    
    # 创建删除db
    manager.add_command("dbc", CreateDB())
    manager.add_command("dbd", DropDB())
    # 更新db
    manager.add_command('db', MigrateCommand)
    # 同步ldap用户
    manager.add_command('ldap', SyncUserldap())
    # 查看当前路由
    manager.add_command('show_urls', commands.ShowUrls())

    manager.add_command('gunicorn', GunicornServer(host="127.0.0.1", port=9000, workers=4))
    manager.add_command("runserver", Server(host="127.0.0.1", port=9000))

    manager.run()