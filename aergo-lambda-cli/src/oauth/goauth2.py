import os
import sys
import yaml
import webbrowser
import colored
import requests
import json

from functools import wraps
from pydrive.auth import GoogleAuth
from colored import stylize
from configure import config

class GoogleOauth2(object):

    # initializing
    def __init__(self):
        self.settingsFile:str = config.LAMB_CONF['goauth2_setting_file_path']+'/'+config.LAMB_CONF['goauth2_setting_file_name']
        self.settings_yaml = yaml.load(open(self.settingsFile,'r'),Loader=yaml.FullLoader)
     
    # get authorization code
    def getResourcePermission(self,settingsYaml=None):
        settingsYaml = self.settingsFile
        gauth = GoogleAuth(settings_file=settingsYaml)
        auth_url = gauth.GetAuthUrl()
        
        # os & 브라우저별 상태관리 필요
        chrome_cmd = "open -a /Applications/Google\ Chrome.app %s"
        webbrowser.get(chrome_cmd).open_new_tab(auth_url)
        print(stylize("Copy & paste the obtained authorization code to login to your Google account.\nPlease close the browser window when done.",colored.fg("green")+colored.attr('bold')))
        auth_code = input('Enter authorization code : ')
        accessToken = GoogleOauth2.getAccessToken(self,auth_code)
        return accessToken

    # get access-token
    def getAccessToken(self,auth_code):
        headers = {
            "Content-Type" : "application/json"
        }
        oauth_url = config.LAMB_CONF['backend_url']+'/oauth2/token'
        oauth_request_data = {
            "provider" : "google",
            "code" : auth_code,
            "redirectUri" : self.settings_yaml['client_config']['redirect_uri'],
            "mode" : "cli"
        }
        oauthResponse = requests.post(oauth_url,json.dumps(oauth_request_data),headers=headers)
        oauthResponseData = json.loads(oauthResponse.text)
        return oauthResponseData['data']

    # login
    def oauth2Login(self,accessToken):
        headers = {
            "Content-Type" : "application/json"
        }
        login_request_data = {
            "provider" : "google",
            "accessToken" : accessToken,
            "mode" : "cli"
        }
        login_url = config.LAMB_CONF['backend_url']+'/oauth2/login'
        loginResponse = requests.post(login_url,json.dumps(login_request_data),headers=headers)
        loginResponseData = json.loads(loginResponse.text)
        return loginResponseData['data']

    # logout
    def oauth2Logout(self):
        headers = {
            "Content-Type" : "application/json",
            "Authorization" : self.getSessionid()
        }
        logoutResponse = requests.post(config.LAMB_CONF['backend_url']+'/oauth2/logout',headers=headers)
        logoutResponseData = json.loads(logoutResponse.text)
        try:           
            if logoutResponseData['status'] is False:
                pass
        except Exception as e:
            print(e)

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
            
if __name__ == "__main__":
    pass
    # print(config.LAMB_CONF['goauth2_setting_file'])
    # gauth = GoogleAuth(settings_file='/Users/kimdohoon/Desktop/aergoLambda/aergoLambdaProject/src/configure/settings.yaml')
    # auth_url = gauth.GetAuthUrl()
    # chrome_cmd = "open -a /Applications/Google\ Chrome.app %s"
    # webbrowser.get(chrome_cmd).open_new_tab(auth_url)
    # print(stylize("Copy & paste the obtained authorization code to login to your Google account.\nPlease close the browser window when done.",colored.fg("green")+colored.attr('bold')))
    # auth_code = input('Enter authorization code : ')
    # token = GoogleOauth2.getAccessToken(auth_code)
    # login_info = GoogleOauth2.oauth2Login(token)
    # print("\nlamb: Wating for login...")
    # print("Logging in ... done")
    # print("Logged in as {}".format(login_info['data']['userName']))
    # print(stylize("Authentication successful.",colored.fg("green")+colored.attr('bold')))
    # oauth2Logout()
    # print(stylize("Success to Logout.",colored.fg("green")+colored.attr('bold')))