#coding=utf-8

from flask import Blueprint, request

from utils.auth import check, authentication
from utils.response import http_code, make_http_response

from .params import RESOURCE
from .service import ModuleService

moduleRouter = Blueprint('module', __name__)


@moduleRouter.route('/list', methods=['GET'])
@authentication()
@check(RESOURCE.module_list_params)
def module_list_view():
    """
    模块列表
    """
    data = request.Data
    flag, result = True, []
    
    if flag:
        return make_http_response(http_code.success, msg='获取项目列表成功', data=result)
    else:
        return make_http_response(http_code.fail, msg='获取项目列表失败' )


@moduleRouter.route('/info', methods=['GET'])
@authentication()
@check(RESOURCE.module_info_params)
def module_info_view():
    """
    模块信息
    """
    data = request.Data
    flag, result = True, []
    
    if flag:
        return make_http_response(http_code.success, msg='获取模块信息成功', data=result)
    else:
        return make_http_response(http_code.fail, msg='获取模块信息失败')


@moduleRouter.route('/add', methods=['POST'])
@authentication()
@check(RESOURCE.module_add_params)
def module_add_view():
    """
    新增模块
    """
    user_id = request.user_id
    data = request.Data

    data['user_id'] = user_id
    module_name = data.get('module_name')
    project_id = data.get('project_id')
    module_service = ModuleService(module_name=module_name, project_id=project_id)

    if module_service.is_module_exist():
        return make_http_response(http_code.success, msg='模块名已存在，请重新命名', data=result)
    else:
        flag, result = module_service.module_add(data)
        if flag:
            return make_http_response(http_code.success, msg='新增模块成功')
        else:
            return make_http_response(http_code.fail, msg='新增模块失败')


@moduleRouter.route('/update', methods=['POST'])
@authentication()
@check(RESOURCE.module_update_params)
def module_update_view():
    """
    更新模块
    """
    data = request.Data
    flag, result = True, []
    
    if flag:
        return make_http_response(http_code.success, msg='编辑模块成功', data=result)
    else:
        return make_http_response(http_code.fail, msg='编辑模块失败')


@moduleRouter.route('/delete', methods=['POST'])
@authentication()
@check(RESOURCE.module_delete_params)
def module_delete_view():
    """
    删除模块
    """
    data = request.Data
    flag, result = True, []
    
    if flag:
        return make_http_response(http_code.success, msg='删除模块成功', data=result)
    else:
        return make_http_response(http_code.fail, msg='删除模块失败')