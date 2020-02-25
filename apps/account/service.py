#coding=utf-8

from utils.logger import logger, auto_log
from utils.tools import gen_passwd, md5
from utils.token import TokenManager
from extra.basic import db
from extra.basic_ldap import myldap

from .models import User, Department


class AccountService(object):
    """
    用户管理类
    """

    def __init__(self, **kwargs):
        self.username = kwargs.get('username') or ''
        user = User.query.filter_by(username=self.username).first() 
        self.id = kwargs.get('user_id') or (user.id if user else '')

    @auto_log
    def is_user_exist(self):
        """
        用户是否存在，用户名唯一
        """
        return True if self.id else False

    @auto_log
    def ldap_auth(self, password):
        """
        认证ldap
        """
        return myldap.auth(self.username, password)
    
    @auto_log
    def comm_auth(self, password):
        """
        系统用户认证
        """
        md5_passwd = md5(password)
        return User.query.filter_by(username=self.username, password=md5_passwd).first()

    @auto_log
    def login(self, password):
        """
        用户登录
        """
        if self.ldap_auth(password) or self.comm_auth(password):
            User.query.filter_by(id=self.id).update({'is_active':True})
            db.session.commit() 
            access_token = TokenManager().create_token(self.id, 360000)
            return True, access_token
        else:            
            return False, ''

    @auto_log
    def logout(self, access_token):
        """
        用户登出
        """
        return TokenManager().del_token(access_token)


    @auto_log
    def get_user_info(self):
        """
        获取用户信息
        """
        user = User.query.filter_by(id=self.id).first()
        if user:
            return True, user.to_json() if user else False
        else:
            return False, ''

    @auto_log
    def list_user(self):
        """
        用户列表
        """
        users = User.query.filter_by(is_active=True).all()
        users_list = [item.to_json() for item in users]
        return True, users_list 

    @auto_log
    def update_user(self, data):
        """
        更新用户
        """
        user = User.query.filter_by(id=self.id).update(data)
        db.session.commit()
        return True, user

    @staticmethod
    def save_user(data):
        """
        保存用户
        """
        user = User(username=data.get('username'),
            password=gen_passwd(),
            email=data.get('email'),
            mobile=data.get('mobile'),
            chinese_name=data.get('chinese_name'),
            ldap_dn=data.get('ldap_dn'),
            )
        db.session.add(user)
        db.session.commit()
        return True, user



class DepartmentService(object):
    """
    部门
    """
    def __init__(self):
        pass
    

    @auto_log
    def list_depart(self):
        """
        部门列表
        """
        departs = Department.query.all()
        departs_list = [item.to_json() for item in departs]
        return True, departs_list

    @staticmethod
    def save_depart(depart):
        """
        新增部门
        """
        department = Department(department=depart)
        db.session.add(department)
        db.session.commit()
        return True, department
