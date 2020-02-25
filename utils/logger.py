#coding=utf-8

import functools
import traceback
import time
import types
import inspect

import logging, logging.handlers

from settings import default

def init_log(log_file=None):
    # 创建一个logger
    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.DEBUG)

    # Create a file handler to store error messages
    fhdr = logging.handlers.TimedRotatingFileHandler(log_file,when='D',interval=1,backupCount=40)
    # fhdr = logging.FileHandler(log_file, mode = 'w')
    fhdr.setLevel(logging.INFO)

    # Create a stream handler to print all messages to console 
    chdr = logging.StreamHandler()
    chdr.setLevel(logging.ERROR)

    # 定义输出格式
    formatter = logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)d] %(funcName)s %(levelname)s %(message)s')
    fhdr.setFormatter(formatter)
    chdr.setFormatter(formatter)

    logger.addHandler(fhdr)
    logger.addHandler(chdr)

    return logger

logger = init_log(log_file=default.LOG_PATH)
# logger.debug("token_debug")
# logger.info("token_info")
# logger.warning("token_warning")
# logger.error("token_error")
# logger.critical("token_ctitical")


def auto_log(func):
    """
    自动记录日志的装饰器
    """
    @functools.wraps(func)
    def _deco(*args, **kwargs):
        try:
            real_func = func(*args, **kwargs)
            return real_func
        except Exception as e:
            logger.error(traceback.format_exc(default.ERROR_LOG_LIMIT))
            time_start = time.time()
            if isinstance(func, types.FunctionType):
                args_spec = inspect.getargspec(func)
                f_user_input = dict(zip(args_spec.args, args))
            else:
                f_user_input = dict()

            f_user_input.update(kwargs)
            logger.error("{}: raw input: {}, timecost: {}ms".format(func.__name__,\
                f_user_input, round((time.time() - time_start)*1000, 2)))
            return False, str(e)

    return _deco
