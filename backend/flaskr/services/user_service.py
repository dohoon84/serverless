import gitlab
import requests
from flaskr.services.gitlab_service import GitlabService
from flaskr.models.user import User
from flask import json, current_app as app

class UserService(GitlabService):

    def check_user(self, email):
        user_by_email = self.gitlab_client.users.list(search=email)

        if not user_by_email:
            return False
        return True

    def create_user(self, User):
        user = User.__dict__
        self.gitlab_client.users.create(user)

    def get_token(self, email, password):
        token_url = app.config['GITLAB_URL'] + '/oauth/token'
        data = {
            "grant_type":"password",
            "username":email,
            "password":password
        }
        response = json.loads(requests.post(token_url, data=data)._content.decode('ascii'))
        return response['access_token']


