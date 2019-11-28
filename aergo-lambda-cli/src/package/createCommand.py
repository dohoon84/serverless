import sys
import gitlab
import colored
import uuid

from functools import wraps
from colored import stylize
from configure import config
from common import repositoryApi
from common import userApi
from . import commonCommand


class CreateCommand(object):

    common = commonCommand.CommonCommand()
    repository = repositoryApi.RepositoryApi()
    user = userApi.UserApi()

    hilight=colored.fg("green") + colored.attr("bold")
    warning = colored.fg("red") + colored.attr("bold")

    # initializing
    def __init__(self):
        self.app_name:str = config.LAMB_CONF['project_name']
        self.serial = None

    # create project method
    def execute(self):
        try:
            self.genAppname()
            r = self.repository.createProject(self.user.getUser,self.app_name)
            self.printResultMsg()
            print("\nIf you have already created your lamb app, you can easily add a remote to your local repository with the git clone & git remote add.\n")
            print(stylize("⬢ Please create new repository (copy & paste)\n",self.hilight),"➡︎ git clone {}".format(self.getGitEndpoint()))
            print(stylize("⬢ Please add git remote repository (copy & paste)\n",self.hilight),"➡︎ git remote add lamb {}".format(self.getGitEndpoint()))
        except SystemError as e:
            print(stylize("\nUnexpected error.\n ➡︎ please send mail to sol1@blocko.io.\n If you are not logged in, please login.",self.warning))
            print(e)
            sys.exit(1)
        except FileNotFoundError as e:
            print(stylize("\nUnexpected error.\n ➡︎ If you are not logged in, please login.",self.warning))
            print(e)
            sys.exit(1)
        else:
            pass

    # print result message
    def printResultMsg(self):
        print(stylize("\nCreating app... done!!! ",self.hilight))
        print(stylize("⬢ app name\n",self.hilight),"➡︎ ",self.app_name)
        print(stylize("⬢ app url\n",self.hilight),"➡︎ ",self.getServiceEndpoint())
        print(stylize("⬢ git endpoint\n",self.hilight),"➡︎ ",self.getGitEndpoint())

    # return service endpoint url
    def getServiceEndpoint(self):
        return ''.join([config.LAMB_CONF['protocol'],self.app_name,".",config.LAMB_CONF['host_name']])

    # return git endpoint url
    def getGitEndpoint(self):
        repoNamespace = self.repository.getRepoNamespace()
        repoToken = self.repository.getRepoToken()
        return ''.join(["http://oauth2:",repoToken,'@',config.LAMB_CONF['host_name'],':',config.LAMB_CONF['port'],'/',repoNamespace,'/',self.app_name,".git"])

    # set app name
    def genAppname(self):
        self.serial = uuid.uuid4()
        self.app_name = ''.join([self.app_name,"-",str(self.serial)[:8]])