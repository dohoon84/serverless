from flaskr.services.google_oauth2_service import GoogleOAuth2Service
from flaskr.services.facebook_oauth2_service import FacebookOAuth2Service

def get_provider(mode, provider_name):
    if provider_name == 'google':
        return GoogleOAuth2Service(mode)
    elif provider_name == 'facebook':
        return FacebookOAuth2Service(mode)