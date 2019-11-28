import sys
import gitlab
import json
import requests

from functools import wraps
from configure import config

class RepositoryApi(object):

    # initializing
    def __init__(self):
        pass

    # createProject
    def createProject(self,user,project_name):
        session = self.getSessionid()
        repo_token = self.getRepoToken()
        headers = {'Content-Type' : 'application/json',
                   'Authorization' : session
        }
        postfix = "@blocko.io"
        email = ''.join([str(user),postfix])
        create_project_url = config.LAMB_CONF['backend_url']+'/projects/'+project_name
        create_project_request_data = {
            "repoToken" : repo_token,
            "email" : email
        }
        projectResponse = requests.post(create_project_url,json.dumps(create_project_request_data),headers=headers)
        projectResponseData = json.loads(projectResponse.text)
        return projectResponseData['data']

    # concate(~/.aergoLambda)
    def join_lamb_file(filename=None):
        def real_decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(''.join([config.LAMB_CONF['user_home'],'/',config.LAMB_CONF['lamb_file_name']]))
            return wrapper
        return real_decorator

    # in .aergo-lambda file
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
    @spliter(delimiter=':', index=1)
    def getSessionid(result):
        return result

    # in .aergo-lambda file
    @spliter(delimiter=':', index=2)
    def getRepoToken(result):
        return result

    # in .aergo-lambda file
    @spliter(delimiter=':', index=3)
    def getRepoNamespace(result):
        return result
