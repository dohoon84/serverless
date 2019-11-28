import uuid
import hashlib
from flaskr.models.result_form import ResultForm
from flaskr.services.oauth2_service import OAuth2Service
from functools import wraps
from flask import jsonify, make_response

def get_name(email):
    return email[0:email.index('@')]

def create_session_id(username):
    raw_id = username + '_' + str(uuid.uuid4())
    hashed_id = hashlib.sha256(raw_id.encode('utf-8')).hexdigest()
    return hashed_id

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not OAuth2Service.is_logged_in():
            result_form = ResultForm()
            result_form.data = {'message':'Login required!'}
            result_form.status = False
            return make_response(jsonify(result_form.serialize()), 401)
        return f(*args, **kwargs)
    return decorated_function
