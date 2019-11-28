import sys
import os

from flask import Flask
from flask_bcrypt import Bcrypt
from .config import config_by_name
from flask_cors import CORS
from flaskr.views import blueprint
from flaskr.websocket import socketio

def create_app(config_name):
  app = Flask(__name__)
  app.config.from_object(config_by_name[config_name])
  app.register_blueprint(blueprint)
  CORS(app, resources={r"/*": {"origins": "*"}})
  socketio.init_app(app, cors_allowed_origins='*', async_mode="gevent")
  return app

def configure_env():
    env = sys.argv[1] if len(sys.argv) > 1 else 'dev'
    if not (env == 'dev' or env == 'prod') :
        env = 'dev'
    return env

