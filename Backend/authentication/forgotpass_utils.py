from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from flask import current_app
from config import Config

def _get_serializer():
    secret = current_app.config.get("SECRET_KEY") or Config.SECRET_KEY
    return URLSafeTimedSerializer(secret)

def generate_password_reset_token(email: str, expires_sec: int = 3600):
    s = _get_serializer()
    salt = current_app.config.get("PASSWORD_RESET_SALT", Config.PASSWORD_RESET_SALT)
    return s.dumps(email, salt=salt)

def verify_password_reset_token(token: str, max_age: int = 3600):
    s = _get_serializer()
    salt = current_app.config.get("PASSWORD_RESET_SALT", Config.PASSWORD_RESET_SALT)
    try:
        email = s.loads(token, salt=salt, max_age=max_age)
        return email
    except (BadSignature, SignatureExpired):
        return None
