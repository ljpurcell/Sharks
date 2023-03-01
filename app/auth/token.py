from itsdangerous import URLSafeTimedSerializer
from app import create_app

app = create_app()

def generate_token(email):
    serializer = URLSafeTimedSerializer(app.config.SECRET_KEY)
    return serializer.dumps(email, salt=app.config.SECURITY_SALT)

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config.SECRET_KEY)
    try:
        email = serializer.loads(token, salt=app.config.SECURITY_SALT, max_age=expiration)
        return email
    except Exception:
        return False