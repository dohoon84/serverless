from flaskr.models.job import Job
from flaskr.models.project import Project
from flaskr.services.gitlab_service import GitlabService
from flask import json, make_response, current_app as app
from flaskr.websocket import socketio

class ProjectService(GitlabService):

    def create_project(self, email, name):
        raw_project = self.gitlab_client.projects.create({'name':name, 'description':name + ' project is for ' + email + '.'})
        project = Project(raw_project.name, raw_project.created_at, raw_project.description)
        return project.__dict__

    def check_project(self, name):
        try :
            raw_project = self.gitlab_client.projects.get(username + '/' + name)
        except Exception :
            return False
        return True  

    def get_project_list(self):
        raw_project_list = self.gitlab_client.projects.list(owned=True)
        project_list = []
        
        for raw_project in raw_project_list:
            project = Project(raw_project.name, raw_project.created_at, raw_project.description)
            project_list.append(project.__dict__)

        return project_list

    def find_project_by_name(self, name):
        raw_project_by_name = self.gitlab_client.projects.list(search=name)[0]
        project = Project(raw_project_by_name.name, raw_project_by_name.created_at, raw_project_by_name.description)
        return project.__dict__

    def get_job_list_by_name(self, name):
        raw_project_by_name = self.gitlab_client.projects.list(search=name)[0]
        raw_job_list = raw_project_by_name.jobs.list()

        job_list = []

        for raw_job in raw_job_list:
            job = Job(raw_job.id, raw_job.name, raw_job.status, raw_job.started_at, raw_job.finished_at, raw_job.duration)
            job_list.append(job.__dict__)

        return job_list

    def get_job_by_name_and_id(self, name, id):
        raw_project_by_name = self.gitlab_client.projects.list(search=name)[0]
        raw_job = raw_project_by_name.jobs.get(id)
        job = Job(raw_job.id, raw_job.name, raw_job.status, raw_job.started_at, raw_job.finished_at, raw_job.duration)
        return job.__dict__

    def trace_job_by_name_and_id(self, name, id):
        raw_project_by_name = self.gitlab_client.projects.list(search=name)[0]
        raw_job = raw_project_by_name.jobs.get(id)
        socketio.emit('log', {'data': raw_job.trace().decode('utf-8')})
