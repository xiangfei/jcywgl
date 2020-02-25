#coding=utf-8

import os

from flask import Blueprint, request, send_from_directory, make_response, send_file

from utils.auth import check, authentication
from utils.response import http_code, make_http_response

from .params import RESOURCE
from .service import ProjectService

projectRouter = Blueprint('project', __name__)


@projectRouter.route('/list', methods=['GET'])
@authentication()
@check(RESOURCE.project_list_params)
def project_list_view():
    """
    项目列表
    """
    data = request.Data

    flag, result = ProjectService.project_list(data)
    if flag:
        return make_http_response(http_code.success, msg='获取项目列表成功', data=result)
    else:
        return make_http_response(http_code.fail, msg='获取项目列表失败' )


@projectRouter.route('/info', methods=['GET'])
@authentication()
@check(RESOURCE.project_info_params)
def project_info_view():
    """
    获取项目
    """
    data = request.Data
    project_id = data.get('id')
    project_service = ProjectService(id=project_id)
    flag, result = project_service.project_info()

    if flag:
        return make_http_response(http_code.success, msg='获取项目成功', data=result)
    else:
        return make_http_response(http_code.fail, msg='获取项目失败')
    

@projectRouter.route('/add', methods=['POST'])
@authentication()
@check(RESOURCE.project_add_params)
def project_add_view():
    """
    新增项目
    """
    user_id = request.user_id
    data = request.Data

    data['user_id'] = user_id
    project_name = data.get('project_name')
    project_service = ProjectService(project_name=project_name)
    if project_service.is_project_exist():
        return make_http_response(http_code.fail, msg='项目名已存在，请重新命名')
    else:
        flag, result = project_service.project_add(data)
        if flag:
            return make_http_response(http_code.success, msg='新增项目成功')
        else:
            return make_http_response(http_code.fail, msg='新增项目失败')



@projectRouter.route('/update', methods=['POST'])
@authentication()
@check(RESOURCE.project_update_params)
def project_update_view():
    """
    更新项目
    """
    data = request.Data
    project_id = data.get('id')

    project_service = ProjectService(id=project_id)
    flag, result = project_service.project_update(data)

    if flag:
        return make_http_response(http_code.success, msg='更新项目成功')
    else:
        return make_http_response(http_code.fail, msg='更新项目失败')


@projectRouter.route('/delete', methods=['POST'])
@authentication()
@check(RESOURCE.project_delete_params)
def project_delete_view():
    """
    删除项目
    """
    data = request.Data
    project_id = data.get('id')

    project_service = ProjectService(id=project_id)
    flag, result = project_service.project_del()

    if flag:
        return make_http_response(http_code.success, msg='删除项目成功')
    else:
        return make_http_response(http_code.fail, msg='删除项目失败')