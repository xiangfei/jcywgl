#coding=utf-8

from datetime import datetime

from extra.basic import db, to_json_ext

roles_dict = {
    '0':'default',
    '1':'admin',
    '2':'dev',
    '3':'test',
    '4':'ops',
    '5':'network',
    '6':'pm'
}

class User(db.Model):
    """
    用户表
    """
    __tablename__ = 'account_user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    chinese_name = db.Column(db.String(32), nullable=True)
    mobile = db.Column(db.String(32), nullable=True)
    ldap_dn = db.Column(db.String(120), nullable=True)

    is_active = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(64), default=0)

    date_updated = db.Column(db.DateTime)
    date_joined = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<User %r>' %(self.username)

    def to_json(self):
        roles_list = []
        for role in list(self.role):
            roles_list.append(roles_dict.get(role))
        return {'id':self.id,   
                'username': self.username,
                'email': self.email,
                'chinese_name': self.chinese_name,
                'mobile': self.mobile or '',
                'role': roles_list,
                'date_joined': self.date_joined.strftime('%Y-%m-%d %H:%M:%S')
            }


class Department(db.Model):
    """
    部门表
    """
    __tablename__ = 'account_department'

    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(32), index=True, unique=True, nullable=False)

    def to_json(self):
        return to_json_ext(self, self.__class__)
