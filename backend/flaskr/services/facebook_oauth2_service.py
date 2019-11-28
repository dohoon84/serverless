import facebook
from flask import current_app as app
from flaskr.services.oauth2_service import OAuth2Service
import requests
import json

class FacebookOAuth2Service(OAuth2Service):
    def __init__(self, mode):
        super(FacebookOAuth2Service, self).__init__(mode, 'facebook')
        self.service = {'client_id': self.client_id, 
                        'client_secret': self.client_secret,
                        'access_token_url': 'https://graph.facebook.com/oauth/access_token',
                        'revoke_token_url': 'https://graph.facebook.com/me/permissions'
                    }

    def get_token(self, code, redirect_uri):
        data = {'code':code, 'client_id':self.service['client_id'], 'client_secret':self.service['client_secret'], 'redirect_uri':redirect_uri}
        raw_response = requests.post(self.service['access_token_url'], json.dumps(data), allow_redirects = False)
        response = json.loads(raw_response.content.decode('utf-8'))
        return response['access_token']

    def revoke_token(self, access_token):
        data = {'access_token':access_token}
        raw_response = requests.delete(self.service['revoke_token_url'], params=data)

    def build_credentials(self, access_token):
        return facebook.GraphAPI(access_token=access_token)

    def get_user_info(self, credentials):
        oauth2_client = credentials
        return oauth2_client.get_object(id='me', fields=['id', 'email'])
       