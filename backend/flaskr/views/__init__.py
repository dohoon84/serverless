from flask import Blueprint, request, make_response, render_template
from flask_restplus import Api, Namespace
from flaskr.services.oauth2_service import OAuth2Service
from flaskr.models.result_form import ResultForm

blueprint = Blueprint('api', __name__)

api = Api(blueprint, title='Aergo Lambda API', doc='/api')

oauth2_api = Namespace('oauth2', description='OAuth2 API')
project_api = Namespace('projects', description='Project API')

api.add_namespace(oauth2_api)
api.add_namespace(project_api)

from flaskr.views import oauth2_view, project_view


    

