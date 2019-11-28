import sys
import colored

from colored import stylize
from . import loginCommand
from . import logoutCommand
from . import createCommand
from functools import wraps

class CommandExecutor(object):

    helpMap = {}
    commandMap = {}
        
    helpMap["login"]  = "login to login server"
    helpMap["logout"] = "logout to login server"
    helpMap["create"] = "create remote repository"

    commandMap["login"] = loginCommand.LoginCommand()
    commandMap["logout"] = logoutCommand.LogoutCommand()
    commandMap["create"] = createCommand.CreateCommand()

    hilight = colored.fg("green") + colored.attr("bold")
    warning = colored.fg("red") + colored.attr("bold")

    # main method
    def execute(self):
        try:
            if len(sys.argv) is 1:
                self.printHelp()
            else:
                commandType = sys.argv[1]
                if commandType in CommandExecutor.commandMap.keys():
                    commandInstance = CommandExecutor.commandMap.get(commandType)
                    if commandInstance == 0:
                        self.printHelp()
                    else:
                        commandInstance.execute()
                else:
                    print(stylize("\nCommand does not exists",CommandExecutor.warning))
        except Exception as e:
            print(stylize("\nInvalid argument",CommandExecutor.warning))
            print(e)
            sys.exit(1)
        else:
            pass

    # print help message
    def printHelp(self):
        print(stylize("\nlamb-cli help\n\nusage:",self.hilight))
        for key in self.helpMap.keys():
            print('\t',stylize(key,self.hilight),self.helpMap[key])