import os
import sys
import colored

from functools import wraps
from colored import stylize
from configure import config
from oauth import goauth2

class LogoutCommand(object):

    goauth = goauth2.GoogleOauth2()

    hilight = colored.fg("green") + colored.attr("bold")
    warning = colored.fg("red") + colored.attr("bold")

    # initializing
    def __init__(self):
        pass
    
    # call logout method
    def execute(self, *args):
        self.logout()

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

    # logout execution
    def logout(self):
        lambFile = self.getLambFilePath()
        if os.path.isfile(lambFile):
            try:
                self.goauth.oauth2Logout()
                print(stylize("\nSuccess to logout ~ :)",self.hilight))
                os.remove(lambFile)
            except IOError as e:
                print(stylize("\nLogout failed",self.warning))
                print(e)
                sys.exit(1)
        else:
            print(stylize("\nNot yet login ~ :(",self.warning))