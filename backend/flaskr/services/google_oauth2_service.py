from flask import current_app as app
from flaskr.services.oauth2_service import OAuth2Service
from google.oauth2.credentials import Credentials
import googleapiclient.discovery
import requests
import json

class GoogleOAuth2Service(OAuth2Service):
    def __init__(self, mode):
        super(GoogleOAuth2Service, self).__init__(mode, 'google')
        self.service = {'client_id': self.client_id, 
                        'client_secret': self.client_secret,
                        'access_token_url': 'https://oauth2.googleapis.com/token',
                        'revoke_token_url': 'https://accounts.google.com/o/oauth2/revoke'
                    }

    def get_token(self, code, redirect_uri):
        data = {'code':code, 'client_id':self.service['client_id'], 'client_secret':self.service['client_secret'], 'redirect_uri':redirect_uri, 'grant_type':'authorization_code'}
        raw_response = requests.post(self.service['access_token_url'], json.dumps(data), allow_redirects = False)
        response = json.loads(raw_response.content.decode('utf-8'))
        return response['access_token']

    def revoke_token(self, access_token):
        data = {'token':access_token}
        raw_response = requests.get(self.service['revoke_token_url'], params=data)

    def build_credentials(self, access_token):
        return Credentials(access_token, client_id=self.service['client_id'], client_secret=self.service['client_secret'], token_uri=self.service['access_token_url'])

    def get_user_info(self, credentials):
        oauth2_client = googleapiclient.discovery.build('oauth2', 'v2', credentials=credentials)
        return oauth2_client.userinfo().get().execute()
       