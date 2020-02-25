#coding=utf-8

from datetime import datetime

from extra.basic import db, to_json_ext


project_type_dict = {
    '1': 'dubbo项目',
    '2': '网关项目'
}


class FrameworkRecord(db.Model):
    """
    脚手架
    """
    __tablename__ = 'res_framework'

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(64), index=True, nullable=False)
    service_name = db.Column(db.String(64), index=True, nullable=False)
    project_type = db.Column(db.Integer, nullable=False)
    down_url = db.Column(db.String(128), nullable=False)
    desc = db.Column(db.String(64), default='', nullable=True)

    date_joined = db.Column(db.DateTime, default=datetime.now)

    def to_json(self):
        return to_json_ext(self, self.__class__)


class ProjectRecord(db.Model):
    """
    项目
    """
    __tablename__ = 'res_project'

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(64), index=True, unique=True, nullable=False)#项目名称
    department_id = db.Column(db.Integer, db.ForeignKey('account_department.id')) #部门ID
    project_stage = db.Column(db.String(8), default='default') #项目状态
    leader_id = db.Column(db.Integer, db.ForeignKey('account_user.id')) #项目负责人
    desc = db.Column(db.String(128)) #项目描述
    
    creator_id = db.Column(db.Integer, db.ForeignKey('account_user.id'))
    date_joined = db.Column(db.DateTime, default=datetime.now)
    date_updated = db.Column(db.DateTime, default=datetime.now)
    is_deleted = db.Column(db.Boolean, default=False)

    def to_json(self):
        return to_json_ext(self, self.__class__)


class ModuleRecord(db.Model):
    """
    项目模块
    """
    __tablename__ = 'res_module'

    id = db.Column(db.Integer, primary_key=True)
    module_name = db.Column(db.String(64), index=True, nullable=False)#模块名称
    project_id = db.Column(db.Integer, db.ForeignKey('res_project.id'))#项目ID
    module_tech = db.Column(db.String(8), nullable=False)#技术栈
    git_url = db.Column(db.String(64), nullable=False)#git地址
    logs_path = db.Column(db.String(64), nullable=False)#日志路径
    module_path = db.Column(db.String(64))#模块路径
    port = db.Column(db.Integer)#端口
    desc = db.Column(db.String(128))#模块描述

    sequence = db.Column(db.Integer)#发布顺序
    module_type = db.Column(db.String(8))#模块类型，基础模块、服务模块、网关模块

    creator_id = db.Column(db.Integer, db.ForeignKey('account_user.id'))
    date_joined = db.Column(db.DateTime, default=datetime.now)
    date_updated = db.Column(db.DateTime, default=datetime.now)
    is_deleted = db.Column(db.Boolean, default=False)

    def to_json(self):
        return to_json_ext(self, self.__class__)






    












