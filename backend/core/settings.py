import os


VK_ACCESS_TOKEN = os.environ.get('VK_ACCESS_TOKEN', '')

TWITTER_API_KEY = os.environ.get('TWITTER_API_KEY', '')
TWITTER_API_SECRET_KEY = os.environ.get('TWITTER_API_SECRET_KEY', '')
TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN', '')
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET', '')

USE_PROXY_SERVER = bool(os.environ.get('USE_PROXY_SERVER', ''))
PROXY_SERVER_IP = os.environ.get('PROXY_SERVER_IP', '')
PROXY_SERVER_PORT = os.environ.get('PROXY_SERVER_PORT', '')
