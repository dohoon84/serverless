from flaskr import create_app, configure_env
from flaskr.websocket import socketio

if __name__ == '__main__':
    app = create_app(configure_env())
    socketio.run(app, host='0.0.0.0', port=app.config['PORT'])

 





