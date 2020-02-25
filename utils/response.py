#coding=utf-8

import json

from flask import json, make_response


class http_code:
    success = {"code":200, "status":"OK"}
    fail = {"code":999, "status":"FAIL"}
    unauth = {"code":400, "status":"UNAUTH"}


def make_http_response(result_dict={}, msg=None, data=None):
    """
    自定义返回结果
    """
    status = msg or result_dict.get("status")
    code = result_dict.get("code")

    data = data if data is not None else {}
    response = make_response(json.dumps({"code":code, "msg":msg, "data":data}))
    response.headers['Content-Type'] = 'application/json;charset=utf-8'
    return response
