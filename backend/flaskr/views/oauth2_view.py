import gitlab
from flask_restplus import Resource
from flaskr.views import oauth2_api
from flask import jsonify, request, make_response
from flaskr.services.oauth2_service_factory import get_provider
from flaskr.services.user_service import UserService
from flaskr.services.session_service import SessionService
from flaskr.models.user import User
from flaskr.models.result_form import ResultForm
from flaskr.utils.utils import login_required, create_session_id

@oauth2_api.route('/token')
class TokenByCode(Resource):
    def post(self):
        provider = request.json['provider']
        mode = request.json['mode']
        code = request.json['code']
        redirect_uri = request.json['redirectUri']

        oauth2_service = get_provider(mode, provider)
        access_token = oauth2_service.get_token(code, redirect_uri)

        result_form = ResultForm()
        result_form.data = access_token
        result_form.status = True

        return make_response(jsonify(result_form.serialize()), 200)  

@oauth2_api.route('/login')
class Login(Resource):           
    def post(self):
        provider = request.json['provider']
        access_token = request.json['accessToken']
        mode = request.json['mode']

        oauth2_service = get_provider(mode, provider)
        credentials = oauth2_service.build_credentials(access_token)
        user_info = oauth2_service.get_user_info(credentials)
        email = user_info['email']

        user_service = UserService()
        user = User(email, provider)
        if not user_service.check_user(email):
           user_service.create_user(user)

        gitlab_access_token = user_service.get_token(user.email, user.password)

        session_service = SessionService()
        session_id = create_session_id(user.username)
        session_user_info = {
            "provider": provider,
            "mode": mode,
            "oauth2Token": access_token,
            "repoToken": gitlab_access_token,
            "email": email
        }
        
        session_service.set_session(session_id, session_user_info)
        
        result_form = ResultForm()
        result_form.data = {
            'userName': user.name,
            'sessionId': session_id,
            'repoToken': gitlab_access_token,
            'repoNamespace': user.username
        }
        result_form.status = True

        return make_response(jsonify(result_form.serialize()), 200)

@oauth2_api.route('/logout')
class Logout(Resource):
    @login_required
    def post(self):
        session_id = request.headers.get('Authorization')
        session_service = SessionService()
        session_service.revoke_session(session_id)

        result_form = ResultForm()
        result_form.status = True
        return make_response(jsonify(result_form.serialize()), 200)
    
