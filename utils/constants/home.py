from .base import SERVICE_BASE_URL

LOGIN_CALLBACK_URL = 'http://localhost:8000/callback'
SSO_LOGIN_URL = f'{SERVICE_BASE_URL}/login?redirectUri={LOGIN_CALLBACK_URL}'
SSO_REGISTER_URL = f'{SERVICE_BASE_URL}/register?redirectUri={SSO_LOGIN_URL}'
