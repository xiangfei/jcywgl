#coding=utf-8

import sys
sys.path.append('..')

from flask import Flask
from werkzeug.utils import import_string

from flask_migrate import Migrate

from settings import default, dev, test, pre, pro
from utils.server import Server

app = Flask(__name__)


class App(Flask):
    """
    APP Factory
    """
    def configure_env(self):
        """
        配置环境变量
        """
        # 加载环境配置
        server_ip = Server().get_server_ip()

        if server_ip in default.PRODUCT_SERVER_IP_LIST:
            self.config.from_object('settings.pro')
        elif server_ip in default.PRE_SERVER_IP_LIST:
            self.config.from_object('settings.pre')
        elif server_ip in default.TEST_SERVER_IP_LIST:
            self.config.from_object('settings.test')
        elif server_ip in default.DEV_SERVER_IP_LIST:
            self.config.from_object('settings.dev')
        else:
            self.config.from_object('settings.default')


    def configure_extensions(self):
        """
        配置扩展模块
        """
        for ext_path in self.config.get('EXTENSIONS', []):
            try:
                ext = import_string(ext_path)
            except Exception as e:
                raise Exception('No {0} extension found:{1}'.format(ext_path,e))

            try:
                if getattr(ext, 'init_app', False):
                    ext.init_app(self)
                else:
                    ext(self)
            except Exception as e:
                raise Exception('{0} extension init error:{1}'.format(ext_path,e))


    def configure_url(self):
        """
        配置路由
        """
        for urls in self.config.get('URLS', []):
            self.register_blueprint(import_string(urls.get('view')), url_prefix=urls.get('url_prefix'))


    def configure_header(self):
        """
        设置header
        """
        @self.after_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Access-Control-Allow-Headers, Authorization'
            # response.headers['Content-Type'] = 'application/json;charset=utf-8'
            return response


    def setup(self):
        self.configure_env()
        self.configure_extensions()
        self.configure_url()
        self.configure_header()


def create_app(app_name):
    app = App(app_name)
    app.setup()

    return app