#auth_routes.py
from flask import Blueprint, request, jsonify
from authentication.auth_services import register_user, login_user
auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/register", methods=["POST"])

def register():
    data = request.get_json() or {}
    # Accept both naming conventions
    user_name = data.get("user_name") or data.get("username")
    user_mail = data.get("user_mail") or data.get("email")
    password = data.get("password")

    resp, code = register_user(user_name=user_name, user_mail=user_mail, password=password)
    return jsonify(resp), code

@auth_bp.route("/login", methods=["POST"])

def login():
    data = request.get_json() or {}
    user_mail = data.get("user_mail") or data.get("email")
    password = data.get("password")

    resp, code = login_user(user_mail=user_mail, password=password)
    return jsonify(resp), code
