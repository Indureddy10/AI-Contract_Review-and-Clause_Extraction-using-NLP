import jwt, datetime
from flask import current_app

def generate_token(user_mail):
    token = jwt.encode(
        {"email": user_mail, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )
    return token
