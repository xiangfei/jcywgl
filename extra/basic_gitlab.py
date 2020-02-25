#coding=utf-8

# http://python-gitlab.readthedocs.io/en/stable/install.html

import gitlab

class GitlabService(object):
    """
    自定义Gitlab
    """
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
        
    def init_app(self, app):
        """
        初始化
        """
        self.gitlab_uri = app.config.get('GITLAB_URI')
        self.gitlab_private_token = app.config.get('GITLAB_PRIVATE_TOKEN')
        self.gl = gitlab.Gitlab(self.gitlab_uri, private_token=self.gitlab_private_token, api_version='4')   

    def add_group(self):
        pass



mygitlab = GitlabService()