from flaskr.services.oauth2_service_factory import get_provider

session = {}

class SessionService:
    def set_session(self, id, user_info):
        session[id] = user_info

    def get_session(self, id):
        return session[id]

    def revoke_session(self, id):
        access_token = session[id]['oauth2Token']
        provider = session[id]['provider']
        mode = session[id]['mode']
        oauth2_service = get_provider(mode, provider)
        oauth2_service.revoke_token(access_token)
        session.pop(id)