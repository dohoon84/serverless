import os
import sys
import json
import requests
import getpass
import colored

from functools import wraps
from colored import stylize
from urllib import parse
from configure import config
from common import userApi
from common import utils

class LoginCommand(object):

    userapi = userApi.UserApi()
    
    hilight = colored.fg("green") + colored.attr("bold")
    warning = colored.fg("red") + colored.attr("bold")

    # initializing
    def __init__(self):
        pass

    #join lamb credentialfile
    def join_lamb_file(filename=None):
        def real_decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(''.join([config.LAMB_CONF['user_home'],'/',config.LAMB_CONF['lamb_file_name']]))
            return wrapper
        return real_decorator

    @join_lamb_file(filename=None)
    def getLambFilePath(result):
        return result

    # login check
    def loginCheck(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            lambFile = LoginCommand.getLambFilePath()
            if os.path.isfile(lambFile):
                user = userApi.UserApi().getUser()
                print(stylize("\nalready loged in as {}".format(user),colored.fg("green")+colored.attr('bold')))
                sys.exit(0)
            return f(*args, **kwargs)
        return decorated

    @loginCheck
    def execute(self, *args):
        try:
            self.createAuthCredentialFile()
            print("\nlamb: Wating for login...")
            print("Welcome to lamb-cli: {}".format(utils.getCurrentStrTime()))
            print("Logging in ... done")
            print("Logged in as {}".format(self.userapi.getUser()))
            print(stylize("Authentication successful.",self.hilight))
        except Exception as e:
            print(stylize("\nIf you haven't resiger account, sign up first. or Check your access token",self.warning))
            sys.exit(1)

    # create lamb credential file
    def createAuthCredentialFile(self):
        try:
            r = self.userapi.goauth2Login()
            userName = r['userName']
            sessionId = r['sessionId']
            repoToken = r['repoToken']
            repoNamespace = r['repoNamespace']
            self.makeAuthTokenFile(userName,sessionId,repoToken,repoNamespace)
        except Exception as e:
            print(e)
            sys.exit(1)
    
    def makeAuthTokenFile(self,userName:str,sessionId:str,repoToken:str,repoNamespace:str):
        try:
            lambFile = self.getLambFilePath()
            f = open(lambFile,"w")
            f.write(userName+':'+sessionId+':'+repoToken+':'+repoNamespace+':'+utils.getCurrentStrTime())
        except FileExistsError as e:
            print(e)
        except IOError as e:
            print(e)
        finally:
            f.close()
            
    """
    create git credential file
    id / password 인증 방식 (legacy)
    """
    # def createGitCredentials(self,user_id:str,password:str):
    #     try:
    #         os.system ('git config --global credential.helper store')
    #         host = "@aergoLambda.io"
    #         delimiter = ":"
    #         encodedId = parse.quote(user_id,encoding='UTF-8')
    #         encodedDelimiter = parse.quote(delimiter,encoding='UTF-8')
    #         encodedPasswd = parse.quote(password,encoding='UTF-8')
    #         f = open(self.config.GIT_CREDENTIAL_FILE_PATH,"w")
    #         git_credential = ''.join([self.config.PROTOCOL,encodedId,delimiter,encodedPasswd,host,str.lower(encodedDelimiter),self.config.PORT])
    #         f.write(git_credential)
    #     except IOError:
    #         print("create git-credentials file io exception")
    #     finally:
    #         f.close()