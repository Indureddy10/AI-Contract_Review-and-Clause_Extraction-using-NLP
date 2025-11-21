# authentication/auth_services.py
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from flask_jwt_extended import create_access_token
from datetime import timedelta
from flask_cors import CORS
0
from database.extensions import db
from database.dbmodels import User
from utils.email_services import send_test_email

def register_user(user_name: str, user_mail: str, password: str):
    """Handles registration logic. Returns (response_dict, status_code)."""
    try:
        if not all([user_name, user_mail, password]):
            return {"status": "error", "message": "All fields are required"}, 400

        existing_user = User.query.filter_by(user_mail=user_mail).first()
        if existing_user:
            return {"status": "error", "message": "Email already registered"}, 409

        hashed_pw = generate_password_hash(password)
        new_user = User(user_name=user_name, user_mail=user_mail, password_hash=hashed_pw)

        db.session.add(new_user)
        db.session.commit()

        # send email but do not block failure of registration
        try:
            send_test_email(user_mail, user_name)
        except Exception as mail_err:
            # Log this in production; we will not fail registration for email issues
            print(f"Failed to send registration email to {user_mail}: {mail_err}")

        return {
            "status": "success",
            "message": "User registered successfully",
            "data": new_user.to_dict()
        }, 201

    except IntegrityError as e:
        db.session.rollback()
        return {
            "status": "error",
            "message": "Database integrity error",
            "details": str(e.orig) if hasattr(e, "orig") else str(e)
        }, 400

    except SQLAlchemyError as e:
        db.session.rollback()
        return {"status": "error", "message": "Database operation failed", "details": str(e)}, 500

    except Exception as e:
        return {"status": "error", "message": "Unexpected error during registration", "details": str(e)}, 500

    finally:
        try:
            db.session.close()
        except Exception:
            pass


def login_user(user_mail: str, password: str):
    """Handles login and returns (response_dict, status_code)."""
    try:
        if not all([user_mail, password]):
            return {"status": "error", "message": "Email and password are required"}, 400

        user = User.query.filter_by(user_mail=user_mail).first()
        if not user or not check_password_hash(user.password_hash, password):
            return {"status": "error", "message": "Invalid email or password"}, 401

        # Generate access token using Flask-JWT-Extended
        access_token = create_access_token(identity=str(user.user_id), expires_delta=timedelta(seconds=3600))

        # Store token in user record (optional)
        user.token = access_token
        db.session.commit()

        return {"status": "success", "message": "Login successful", "token": access_token, "data": user.to_dict()}, 200

    except Exception as e:
        db.session.rollback()
        return {"status": "error", "message": "Unexpected error during login", "details": str(e)}, 500

    finally:
        try:
            db.session.close()
        except Exception:
            pass
