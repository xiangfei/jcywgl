#coding=utf-8
import os
from datetime import datetime

from utils.logger import logger, auto_log
from apps.account.models import Department
from .models import db, FrameworkRecord, ProjectRecord


class FrameService(object):
    """
    脚手架服务类
    """
    def __init__(self, **kwargs):
        self.project_name = kwargs.get('project_name','')
        self.service_name = kwargs.get('service_name','')
        self.project_type = kwargs.get('project_type','')
        self.desc = kwargs.get('desc', '')
        framework = FrameworkRecord.query.filter_by(
            project_name=self.project_name,
            service_name=self.service_name,
            project_type=self.project_type
        ).first() 
        self.id = kwargs.get('id') or (framework.id if framework else '')
    
    def is_frame_exist(self):
        """
        是否存在
        """
        return True if self.id else False 

    @auto_log
    def save_frame(self):
        """
        生成框架打包
        """
        cmd = 'cd {0}/script/jcwf/ && python2 project_gen_args.py {1} {2} {3}'.format(os.getcwd(), 
            self.project_name, self.service_name, self.project_type)
        result = os.system(cmd)
        if 0 == result:
            filename = self.project_name + '-' + self.service_name + '.zip'
            down_url = 'http://jcywgl.jc/api/v1.0/framework/download?filename={0}'.format(filename)
            try:
                framework = FrameworkRecord(project_name=self.project_name, 
                    service_name=self.service_name, 
                    project_type=int(self.project_type),
                    down_url=down_url,
                    desc=self.desc
                )
                db.session.add(framework)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                os.system('rm -rf {0}/downloads/{1}'.format(os.getcwd(), filename))
                logger.error(e)
                return False, ''
            return True, down_url
        else:
            return False, ''
    
    @staticmethod
    @auto_log
    def frame_list(params):
        """
        获取列表
        """
        page = params.get('page')
        limit = params.get('limit')
    
        frameworks = FrameworkRecord.query.paginate(int(page), int(limit), False)
        frame_all = FrameworkRecord.query.all()

        frame_list = [item.to_json() for item in frameworks.items]
        result = {
            'items': frame_list,
            'total': len(frame_all)
        }
        return True, result


class ProjectService(object):
    """
    项目类
    """
    def __init__(self, **kwargs):
        self.project_name = kwargs.get('project_name','')
        self.project = ProjectRecord.query.filter_by(project_name=self.project_name).first()
        self.id = kwargs.get('id', '') or (self.project.id if self.project else '')

    def is_project_exist(self):
        """
        项目是否存在
        """
        return True if self.id else False

    @auto_log
    def project_info(self):
        """
        项目信息
        """
        project = ProjectRecord.query.filter_by(id=self.id).first()
        
        return True, project.to_json()

    @auto_log
    def project_add(self, params):
        """
        新增项目
        """
        project = ProjectRecord(project_name=params.get('project_name'),
            department_id = params.get('department_id'),
            project_stage = params.get('project_stage'),
            leader = params.get('leader_id'),
            desc = params.get('desc'),
            creator_id = params.get('user_id')
        )
        db.session.add(project)
        db.session.commit()
        return True, ''

    @auto_log
    def project_update(self, params):
        """
        更新项目
        """
        params['date_updated'] = datetime.now()
        project = ProjectRecord.query.filter_by(id=self.id).update(params)
        db.session.commit()
        return True, project

    @auto_log
    def project_del(self):
        """
        删除项目
        """
        project = ProjectRecord.query.filter_by(id=self.id).update(
            {'is_deleted':True, 'date_updated':datetime.now()})
        db.session.commit()
        return True, project

    @staticmethod
    @auto_log
    def project_list(params):
        """
        获取列表
        """
        page = params.get('page')
        limit = params.get('limit')
        project_name = params.get('project_name') or ''
        department_id = params.get('department_id') or ''
    
        if project_name or department_id:
            sql_args = (ProjectRecord.department_id==department_id)|(ProjectRecord.project_name.like('%'+project_name+'%' if project_name else ''))
        else:
            sql_args = ''
            
        projects = ProjectRecord.query.filter_by(is_deleted=False).filter(sql_args).paginate(int(page), int(limit), False)

        project_list = [item.to_json() for item in projects.items]
        project_all = ProjectRecord.query.filter_by(is_deleted=False).all()
        result = {
            'items': project_list,
            'total': len(project_all)
        }
        return True, result


class ModuleService(object):
    """
    模块类
    """
    def __init__(self, **kwargs):
        self.module_name = kwargs.get('module_name','')
        self.project_id = kwargs.get('project_id','')
        self.module = ModuleRecord.query.filter_by(project_id=self.project_id, module_name=self.module_name).first()
        self.id = kwargs.get('id', '') or (self.module.id if self.module else '')
    
    def is_module_exist(self):
        """
        模块是否存在
        """
        return True if self.id else False

    @auto_log
    def module_add(self, params):
        """
        新增模块
        """
        module = ModuleRecord(module_name=params.get('module_name'),
            project_id = params.get('project_id'),
            project_stage = params.get('project_stage'),
            leader = params.get('leader_id'),
            desc = params.get('desc'),
            creator_id = params.get('user_id')
        )
        db.session.add(module)
        db.session.commit()
        return True, ''
