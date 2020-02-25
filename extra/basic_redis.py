#coding=utf-8

import redis

class RedisService(object):
    """
    自定义Redis驱动类
    """
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        初始化redis
        """
        REDIS_SERVER = {
            'accessToken':{
                "host": app.config.get('REDIS_HOST'),
                "port": app.config.get('REDIS_PORT'),
                "password": app.config.get('REDIS_PASSWORD'),
                "db": 0
            }
        }
        self.redis_token = redis.Redis(connection_pool=redis.ConnectionPool(**REDIS_SERVER.get('accessToken')))
    
    def get_redis_token(self):
        """
        获取redis_token
        """
        return self.redis_token


myredis = RedisService()
