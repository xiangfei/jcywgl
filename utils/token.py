#coding=utf-8

import json

from extra.basic_redis import myredis
from utils.tools import make_uid

class TokenManager(object):
    """
    token 管理
    """
    def __init__(self):
        self.redis_token = myredis.get_redis_token()
    
    def create_token(self, user_id, time):
        """
        生成令牌
        """
        access_token = make_uid()
        new_key = 'access_token:'+access_token+'#'+str(user_id)
        value = json.dumps({
            'user_id':user_id,
        })
        
        old_keys = self.redis_token.keys('*#'+str(user_id)) 
        if old_keys:
            self.redis_token.delete(*old_keys)
        self.redis_token.setex(new_key, value, time)
        return access_token


    def del_token(self, access_token):
        """
        删除令牌
        """
        self.redis_token.delete('access_token:'+access_token)
        return True