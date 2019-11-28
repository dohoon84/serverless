import gitlab
from flask import current_app as app

class GitlabService:
    def __init__(self):
        self.gitlab_client = gitlab.Gitlab(app.config['GITLAB_URL'], app.config['GITLAB_TOKEN'])