#coding=utf-8

from flask import Blueprint, request

from utils.auth import check, authentication
from utils.response import http_code, make_http_response

from .params import ACCOUNT
from .service import AccountService, DepartmentService

accountRouter = Blueprint('account', __name__)

#####user

@accountRouter.route('/login', methods=['POST'])
@check(ACCOUNT.login)
def login():
    """
    用户登录
    """
    data = request.Data
    username = data.get('username')
    password = data.get('password')

    account_service = AccountService(username=username)
    
    if account_service.is_user_exist():
        flag, access_token = account_service.login(password)
        if flag:
            return make_http_response(http_code.success, msg='登录成功', data={'token':access_token})
        else:
            return make_http_response(http_code.fail, msg='用户名或密码错误')
    else:
        return make_http_response(http_code.fail, msg='用户名不存在')


@accountRouter.route('/info', methods=['GET'])
@authentication()
def info():
    """
    用户信息
    """
    user_id = request.user_id

    flag, result = AccountService(user_id=user_id).get_user_info()
    
    if flag:
        return make_http_response(http_code.success, msg='获取用户信息成功', data=result)
    else:
        return make_http_response(http_code.fail, msg='获取用户信息失败') 


@accountRouter.route('/list', methods=['GET'])
@authentication()
def user_list_view():
    """
    用户列表
    """
    flag, result = AccountService().list_user()

    if flag:
        return make_http_response(http_code.success, msg='获取用户列表成功', data=result)
    else:
        return make_http_response(http_code.success, msg='获取用户列表成功', data=result)


@accountRouter.route('/logout', methods=['POST'])
@authentication()
def logout():
    """
    用户登出
    """
    user_id = request.user_id
    access_token = request.access_token
    
    flag = AccountService(user_id=user_id).logout(access_token)
    if flag:
        return make_http_response(http_code.success, msg='登出成功')
    else:
        return make_http_response(http_code.fail, msg='登出失败')


#####department

@accountRouter.route('/department/list', methods=['GET'])
@authentication()
def department_list():
    """
    部门列表
    """
    flag, result = DepartmentService().list_depart()

    if flag:
        return make_http_response(http_code.success, msg='获取部门列表成功', data=result)
    else:
        return make_http_response(http_code.fail, msg='获取部门列表失败')