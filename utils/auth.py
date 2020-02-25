#coding=utf-8

import re
import json
from functools import wraps

from flask import request

from utils.response import http_code, make_http_response
from extra.basic_redis import myredis


def authentication():
    """
    认证用户是否登录
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            redis_token = myredis.get_redis_token()

            access_token = request.headers.get('Authorization') or request.cookies.get('AUID')
            if not access_token:
                return make_http_response(http_code.unauth, '认证失败，请重新登录')

            keys = redis_token.keys('access_token:'+access_token+'#*')
            if not keys:
                return make_http_response(http_code.unauth, '认证失败，请重新登录')
            else:
                key = keys[0]
            
            value = json.loads(redis_token.get(key))
            user_id = value.get('user_id')

            request.user_id = user_id
            request.access_token = access_token
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

                
def check(params):
    """
    根据传入的字段元数据，校验API调用者的传入数据。
    自动补全可空字段，将数据作为一个字典，通过request传入API

    使用例子：
        test_dic = [
                {"name":"name","nullable":False,"regx":r"^(\d)$"},
                {"name":"age","default":"abcde"}
                ]

        @app.route('/test/',methods=['GET','POST'])
        @check(test_dic)
        def test():
            return json.dumps(request.Data)
    可描述字段：
        name:字段名称
        nullable(optional)：是否可空
        default(optional)：默认值，前提为可空
        regx(optional)：该参数的正则表达式

    提示:
        如果参数为可空，并且没有默认值，则从Data中取到为None

    :param paras::字段元数据描述
    :return:
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = dict()
            for item in params:
                param_name = item['name']
                if request.method == 'POST':
                    _data = request.json.get(param_name) or item.get('default')
                else:
                    _data = request.form.get(param_name) or request.args.get(param_name) or item.get('default')

                if not item.get('nullable', True) and not _data:
                    return make_http_response(http_code.fail, 'parameter {0} is required'.format(param_name))
                if _data and item.get('regx') and not re.match(item['regx'], str(_data)):
                    return make_http_response(http_code.fail, 'parameter {0} is illegal'.format(param_name))
                data[param_name] = _data
                
            request.Data = data
            return func(*args, **kwargs)
        return wrapper
    return decorator