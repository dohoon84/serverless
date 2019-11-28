import sys
import requests
import json

from functools import wraps
from configure import config
from oauth import goauth2

class UserApi(object):

    oauth = goauth2.GoogleOauth2()

    # initializing
    def __init__(self):
        pass

    # google oauthLogin
    def goauth2Login(self):
        try:
            accessToken = self.oauth.getResourcePermission()
            data = self.oauth.oauth2Login(accessToken)
            return data
        except Exception as e:
            print(e)
    
    # google oauth2Logout
    def goauth2Logout(self):
        self.oauth.oauth2Logout()

    # concate(~/.aergoLambda)
    def join_lamb_file(filename=None):
        def real_decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(''.join([config.LAMB_CONF['user_home'],'/',config.LAMB_CONF['lamb_file_name']]))
            return wrapper
        return real_decorator

    # return .aergo-labmda
    @join_lamb_file(filename=None)
    def getLambFilePath(result):
        return result

    # delimiter split job
    def spliter(filename=getLambFilePath(), delimiter=None, index=None):
        def real_decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                f = open(filename)
                r = f.readlines()
                return func(''.join(r).split(delimiter)[index])
            return wrapper
        return real_decorator
    
    # in .aergo-lambda file
    @spliter(delimiter=':', index=0)
    def getUser(result):
        return result