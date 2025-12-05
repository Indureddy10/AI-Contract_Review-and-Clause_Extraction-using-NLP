from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_jwt_extended import JWTManager

# Global instances (initialized once)
db = SQLAlchemy()
mail = Mail()
jwt = JWTManager()