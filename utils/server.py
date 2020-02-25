#coding=utf-8

import platform
import socket
import fcntl
import struct
import subprocess
import tempfile


class Server(object):
    '''
    当前服务器的类
    '''
    def __init__(self):
        pass

    def get_server_ip(self):
        """
        获取当前服务器地址
        """
        try:
            if platform.system() == 'Windows':
                ip = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
            elif platform.system() == 'Linux':  # 获取eth0网卡地址
                def get_ip_address():
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        s.connect(('8.8.8.8', 80))
                        ip = s.getsockname()[0]
                    finally:
                        s.close()
                    return ip
                ip = get_ip_address()
            else:
                ip = '127.0.0.1'
            return ip
        except Exception as e:            
            raise Exception('获取当前服务器地址异常:{0}'.format(e))

    @classmethod
    def run_local_command(cls, cmd_str, code_out=False, readlines=True, cwd=None):
        """
        执行本地命令
        """
        if cmd_str in ['rm -rf ', 'rm -rf /']:
            return False, 'can not exec this cmd: %s' % cmd_str

        out_temp = tempfile.SpooledTemporaryFile(buffering=10*1000)
        file_no = out_temp.fileno()
        obj = subprocess.Popen(cmd_str, stdout=file_no, shell=True, cwd=cwd)
        return_code = obj.wait()

        if readlines:
            out = out_temp.readlines()
            out = map(lambda item: str(item.strip()), out)
        else:
            out = str(out_temp.read())
        
        
    

        

