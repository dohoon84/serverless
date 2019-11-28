from flask import request, current_app as app
from flask import request

class OAuth2Service:

    def __init__(self, mode, provider_name):
        self.provider_name = provider_name
        self.credentials = app.config['OAUTH_CREDENTIALS'][mode][provider_name]
        self.client_id = self.credentials['client_id']
        self.client_secret = self.credentials['client_secret']

    def is_logged_in():
        if request.headers.get('Authorization') == '':
            return False
        else:
            return True

    def get_token(self, code, redirect_uri):
        pass

    def revoke_token(self, access_token):
        pass

    def build_credentials(self, token):
        pass

    def get_user_info(self, credentials):
        pass

  

