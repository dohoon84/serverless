import os
import sys

# lamb configuration
LAMB_CONF = {
    'lamb_file_name': '.aergo-lambda',
    'protocol': 'http://',
    'host_name': 'aergoLambda.io',
    'port': '10080',
    'endpoint': 'http://aergoLambda.io:10080',
    'backend_url': 'http://aergoLambda.io:8080',
    'project_name': 'lamb-fresh',
    'user_home': os.getenv('HOME'),
    'goauth2_setting_file_path': os.path.dirname(os.path.abspath(__file__)),
    'goauth2_setting_file_name': 'goauth2Settings.yaml'
}

if __name__ == "__main__":
    print(LAMB_CONF['lamb_file_name'])
    # print(LAMB_CONF['settings'])
    print(os.path.dirname( os.path.abspath( __file__ ) ))
