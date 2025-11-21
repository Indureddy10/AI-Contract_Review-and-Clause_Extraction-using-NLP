# documents/doc_services.py

import os
import uuid
from datetime import datetime
from flask import request
from PyPDF2 import PdfReader
import docx
from werkzeug.utils import secure_filename
from database.extensions import db
from database.dbmodels import Document

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "..", "uploads")
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}


def allowed_file(name):
    return "." in name and name.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# 1️⃣ Upload document
def upload_document(user_id: str):
    try:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        if "file" not in request.files:
            return {"status": "error", "message": "No file in request"}, 400

        file = request.files["file"]
        if not file.filename:
            return {"status": "error", "message": "No file selected"}, 400

        if not allowed_file(file.filename):
            return {"status": "error", "message": "Unsupported file type"}, 400

        ext = file.filename.rsplit(".", 1)[1].lower()
        unique_name = f"{uuid.uuid4()}.{ext}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_name)
        file.save(file_path)

        # FIXED: Use correct model and correct variable names
        new_doc = Document(
            user_id=user_id,
            doc_name=file.filename,
            doc_type=ext,
            doc_size=os.path.getsize(file_path),
            file_path=file_path,
            status="Uploaded",
            uploaded_at=datetime.utcnow()
        )

        db.session.add(new_doc)
        db.session.commit()

        return {"status": "success", "message": "File uploaded", "data": new_doc.to_dict()}, 201

    except Exception as e:
        db.session.rollback()
        return {"status": "error", "message": str(e)}, 500


# 2️⃣ Process and clean document for summary & extraction
def process_document(doc_id):
    try:
        document = Document.query.get(doc_id)
        if not document:
            return {"status": "error", "message": "Document not found"}, 404

        document.status = "Processing"
        db.session.commit()

        raw_content = extract_text(document.file_path)
        cleaned_text = clean_text(raw_content)

        document.raw_text = cleaned_text
        document.status = "Complete"
        db.session.commit()

        return {"status": "success", "message": "Processing complete", "raw_text": cleaned_text}, 200

    except Exception as e:
        document.status = "Error"
        db.session.rollback()
        return {"status": "error", "message": str(e)}, 500


# 3️⃣ Extract text from PDF/DOCX/TXT
def extract_text(file_path):
    ext = file_path.rsplit(".", 1)[1].lower()

    if ext == "pdf":
        text = ""
        reader = PdfReader(file_path)
        for page in reader.pages:
            extracted = page.extract_text() or ""
            text += extracted
        return text

    if ext == "docx":
        doc = docx.Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])

    if ext == "txt":
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    return ""


# 4️⃣ Clean text for summarization and key feature extraction
def clean_text(text: str):
    if not text:
        return ""

    # Remove extra spaces
    text = text.replace("\n", " ").replace("\t", " ")
    text = " ".join(text.split())
    
    # Optional: Remove special unwanted characters if needed
    # import re
    # text = re.sub(r"[^A-Za-z0-9.,;:!?()\- ]", "", text)

    return text
