# app.py
import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import NoAuthorizationError
from werkzeug.exceptions import HTTPException
from flask_cors import CORS

load_dotenv()

from database.config import Config
from database.extensions import db, mail, jwt
from authentication.auth_routes import auth_bp
from documents.doc_routes import doc_bp
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    app.register_blueprint(doc_bp, url_prefix="/api/doc")

    
    # Simple home
    @app.route("/")
    def home():
        return jsonify({"message": "Welcome to the Flask app!"})

    
    # Optional: nicer JSON 404
    @app.errorhandler(404)
    def not_found(err):
        return jsonify({"error": "Route not found"}), 404
    
    @jwt.unauthorized_loader
    def unauthorized_response(callback):
       return jsonify({"error": "Missing or invalid token"}), 401

    

    @app.errorhandler(Exception)
    def handle_exception(e):
       if isinstance(e, HTTPException):
           return jsonify(error=str(e)), e.code
       return jsonify(error="Server error", message=str(e)), 500

    return app

if __name__ == "__main__":
    app = create_app()
    # Create DB tables in dev if using sqlite/local
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=int(os.getenv("PORT", 5000)))
