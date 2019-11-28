import os

class Config:
    PORT = 8080
    SECRET_KEY = os.urandom(16)
    OAUTH_CREDENTIALS = {
        'cli':{
                'google': {
                'client_id': '1033452540986-9sfqueasb12v3ll4rn6l8m517ebvjdut.apps.googleusercontent.com',
                'client_secret': 'ytqoyJLOM_uxNl7XSuM5-pT8',
            },
                'facebook': {
                'client_id': 'xxxxxxx',
                'client_secret': 'xxxxxxxxxxx'
            }
        },
        'web':{
                'google': {
                'client_id': '658236964299-3u3o2hbht87m843su2da6vuc9prfvspp.apps.googleusercontent.com',
                'client_secret': 'mVFVRmBn6IF9Tb21y1Ka_uzv',
            },
                'facebook': {
                'client_id': '268712036878831',
                'client_secret': 'c5f9e6b6d9475c763d2588f8bf71edd8'
            }
        }
        
    }
    # local gitlab url : 'http://aergolambda.io:10080'
    GITLAB_URL = 'http://192.168.1.106:10080'
    # local gitlab token : 'xQ4uxS9ZVhHSY8J-cDG7'
    GITLAB_TOKEN = 'jrAbxpk5aZN7tHoLadFa'
    GITLAB_SECRET = 'blocko123!'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)
        
