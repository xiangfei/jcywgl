#coding=utf-8

import os

from flask import Blueprint, request, send_from_directory, make_response, send_file

from utils.auth import check, authentication
from utils.response import http_code, make_http_response

from .params import RESOURCE
from .service import FrameService

frameworkRouter = Blueprint('frame', __name__)


@frameworkRouter.route('/init', methods=['POST'])
@authentication()
@check(RESOURCE.initframe)
def framework_init_view():
    """
    生成项目脚手架
    """
    data = request.Data
    project_name = data.get('project_name')
    service_name = data.get('service_name')
    project_type = data.get('project_type')
    description = data.get('remark')
    frame_service = FrameService(project_name=project_name,
        service_name=service_name,
        project_type=project_type,
        desc=description
    )

    if frame_service.is_frame_exist():
        return make_http_response(http_code.fail, msg='创建失败，该项目已存在')
    else:
        flag, result = frame_service.save_frame()
        if flag:
            return make_http_response(http_code.success, msg='初始化项目成功', data={'url': result})
        else:
            return make_http_response(http_code.fail, msg='初始化项目失败')


@frameworkRouter.route('/download', methods=['GET'])
@authentication()
def framework_down_view():
    """
    下载脚手架
    """
    filename = request.args.get('filename')

    response = make_response(send_file(os.getcwd()+'/downloads/'+filename))
    response.headers["Content-Disposition"] = "attachment; filename="+filename

    return response


@frameworkRouter.route('/list', methods=['GET'])
@authentication()
@check(RESOURCE.listframe)
def framework_list_view():
    """
    获取脚手架列表
    """
    data = request.Data

    flag, result = FrameService.frame_list(data)

    if flag:
        return make_http_response(http_code.success, msg='获取脚手架列表成功', data=result)
    else:
        return make_http_response(http_code.fail, msg='获取脚手架列表失败')



