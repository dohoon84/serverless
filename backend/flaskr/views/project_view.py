import gitlab
from flask_restplus import Resource
from flaskr.views import project_api
from flask import request, jsonify, make_response, current_app as app
from flaskr.models.result_form import ResultForm
from flaskr.services.project_service import ProjectService
from flaskr.services.oauth2_service import OAuth2Service
from flaskr.services.session_service import SessionService
from flaskr.utils.utils import login_required
from flask_socketio import emit
from flaskr.websocket import socketio

@project_api.route('')
class ProjectList(Resource):
    @login_required
    def get(self):
        session_id = request.headers.get('Authorization')
        session_service = SessionService()
        user_info = session_service.get_session(session_id)

        project_service = ProjectService()
        gitlab_token = user_info['repoToken']
        email = user_info['email']
        project_service.gitlab_client = gitlab.Gitlab(app.config['GITLAB_URL'], oauth_token=gitlab_token)
        
        project_list = project_service.get_project_list()

        result_form = ResultForm()
        result_form.data = project_list
        result_form.status = True

        return make_response(jsonify(result_form.serialize()), 200)

@project_api.route('/<project_name>')
class ProjectByName(Resource):
    @login_required
    def get(self, project_name):
        session_id = request.headers.get('Authorization')
        session_service = SessionService()
        user_info = session_service.get_session(session_id)

        project_service = ProjectService()
        gitlab_token = user_info['repoToken']
        project_service.gitlab_client = gitlab.Gitlab(app.config['GITLAB_URL'], oauth_token=gitlab_token)
        
        project = project_service.find_project_by_name(project_name)

        result_form = ResultForm()
        result_form.data = project
        result_form.status = True

        return make_response(jsonify(result_form.serialize()), 200)

    @login_required
    def post(self, project_name):
        session_id = request.headers.get('Authorization')
        session_service = SessionService()
        user_info = session_service.get_session(session_id)

        email = user_info['email']
        gitlab_token = user_info['repoToken']

        project_service = ProjectService()
        project_service.gitlab_client = gitlab.Gitlab(app.config['GITLAB_URL'], oauth_token=gitlab_token)

        result_form = ResultForm()
        response = ''
        if not project_service.check_project(project_name):
           project = project_service.create_project(email, project_name)
           result_form.data = project
           result_form.status = True
           response = 200
        else:
           result_form.data = {'message': project_name + ' is dupulicated!'}
           result_form.status = False
           response = 400

        return make_response(jsonify(result_form.serialize()), response)

@project_api.route('/<project_name>/jobs')
class JobListByProject(Resource):
    @login_required
    def get(self, project_name):
        session_id = request.headers.get('Authorization')
        session_service = SessionService()
        user_info = session_service.get_session(session_id)

        project_service = ProjectService()
        gitlab_token = user_info['repoToken']
        project_service.gitlab_client = gitlab.Gitlab(app.config['GITLAB_URL'], oauth_token=gitlab_token)
        
        job_list = project_service.get_job_list_by_name(project_name)

        result_form = ResultForm()
        result_form.data = job_list
        result_form.status = True

        return make_response(jsonify(result_form.serialize()), 200)

@project_api.route('/<project_name>/jobs/<job_id>')
class JobByProjectNameAndId(Resource):
     @login_required
     def get(self, project_name, job_id):
        session_id = request.headers.get('Authorization')
        session_service = SessionService()
        user_info = session_service.get_session(session_id)

        project_service = ProjectService()
        gitlab_token = user_info['repoToken']
        project_service.gitlab_client = gitlab.Gitlab(app.config['GITLAB_URL'], oauth_token=gitlab_token)
        
        job = project_service.get_job_by_name_and_id(project_name, job_id)

        result_form = ResultForm()
        result_form.data = job
        result_form.status = True

        return make_response(jsonify(result_form.serialize()), 200)

@project_api.route('/<project_name>/jobs/<job_id>/trace')
class JobLog(Resource):
     @login_required
     def get(self, project_name, job_id):
        session_id = request.headers.get('Authorization')
        session_service = SessionService()
        user_info = session_service.get_session(session_id)
        
        project_service = ProjectService()
        gitlab_token = user_info['repoToken']
        project_service.gitlab_client = gitlab.Gitlab(app.config['GITLAB_URL'], oauth_token=gitlab_token)
        
        job = project_service.trace_job_by_name_and_id(project_name, job_id)

        result_form = ResultForm()
        result_form.data = job.decode('utf-8')
        result_form.status = True

        return make_response(jsonify(result_form.serialize()), 200)

@socketio.on('connect')
def connect():
    print('connected!')

@socketio.on('request')
def trace_job_by_name_and_id():
    session_id = request.args.get('Authorization')
    session_service = SessionService()
    project_name = request.args.get('projectName')
    job_id = request.args.get('jobId')

    user_info = session_service.get_session(session_id)
        
    project_service = ProjectService()
    gitlab_token = user_info['repoToken']
    project_service.gitlab_client = gitlab.Gitlab(app.config['GITLAB_URL'], oauth_token=gitlab_token)
    project_service.trace_job_by_name_and_id(project_name, job_id)

@socketio.on('disconnect')
def disconnect():
    print('disconnected!')








    






