from flaskr.utils import utils
from flask import current_app as app

class User:
    def __init__(self, email, provider):
        self.email = email
        self.password = app.config['GITLAB_SECRET']
        self.username = utils.get_name(self.email) + '_' + provider 
        self.name = utils.get_name(self.email)
        self.skip_confirmation = True
