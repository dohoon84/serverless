import os
import sys
import gitlab

from configure import config
from common import userApi
from functools import wraps

class CommonCommand(object):
    
    userApi = userApi.UserApi()

    # initializing
    def __init__(self):
        pass

    # concate(~/.aergoLambda)
    def join_lamb_file(filename=None):
        def real_decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(''.join([config.LAMB_CONF['user_home'],'/',config.LAMB_CONF['lamb_file_name']]))
            return wrapper
        return real_decorator

    @join_lamb_file(filename=None)
    def getAuthToken(result):
        try:
            f = open(result, "r")
            accessToken = f.readline()
            return accessToken
        except FileNotFoundError as e:
            print("accessToken file not found : {}".format(e))
            sys.exit(1)
        except IOError as e:
            print("io exception : {}".format(e))
            sys.exit(1)
        finally:
            f.close()