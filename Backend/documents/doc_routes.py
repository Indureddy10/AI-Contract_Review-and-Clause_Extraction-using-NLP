# documents/doc_routes.py

from flask import Blueprint, request, jsonify
from documents.doc_services import upload_document, process_document
from flask_jwt_extended import jwt_required,get_jwt_identity
from database.dbmodels import Document
from database.extensions import db

doc_bp = Blueprint("document_bp", __name__)


# 1️⃣ Upload File
@doc_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload_file():
    user_id = get_jwt_identity()     # <-- FIXED

    if not user_id:
        return jsonify({"status": "error", "message": "Invalid token or user not found"}), 401

    response, status = upload_document(user_id)
    return jsonify(response), status

# 2️⃣ Process Uploaded File
@doc_bp.route("/process/<uuid:doc_id>", methods=["POST"])
@jwt_required()
def process_file(doc_id):
    response, status = process_document(doc_id)
    return jsonify(response), status


# 3️⃣ Get Extracted/Cleaned Raw Text
@doc_bp.route("/extract/<uuid:doc_id>", methods=["GET"])
@jwt_required()
def extract_raw_text(doc_id):
    document = Document.query.get(doc_id)

    if not document:
        return jsonify({"status": "error", "message": "Document not found"}), 404

    return jsonify({
        "status": "success",
        "data": {
            "doc_id": str(document.doc_id),
            "status": document.status,
            "raw_text": document.raw_text
        }
    }), 200


# 4️⃣ OPTIONAL: Delete a document
@doc_bp.route("/delete/<uuid:doc_id>", methods=["DELETE"])
@jwt_required()
def delete_document(doc_id):
    document = Document.query.get(doc_id)
    if not document:
        return jsonify({"status": "error", "message": "Document not found"}), 404

    try:
        db.session.delete(document)
        db.session.commit()
        return jsonify({"status": "success", "message": "Document deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    

