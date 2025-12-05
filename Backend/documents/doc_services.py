import os
import uuid
import re
import logging
import io
from datetime import datetime

# Flask & Utils
from flask import request
from werkzeug.utils import secure_filename

# Database
from database.extensions import db
from database.models import Document

# NLP Engine
from nlp_engine.processor import process_document_by_id

# Libraries for PDF/OCR
import fitz  # PyMuPDF
import pytesseract
import docx
from PIL import Image

# --- CONFIGURE LOGGING ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- CONFIGURATION: TESSERACT PATH ---
# CRITICAL: Verify this path matches your installation
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

if os.path.exists(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
    logger.info(f"Tesseract found at: {TESSERACT_PATH}")
else:
    logger.warning(f"⚠️ TESSERACT NOT FOUND AT {TESSERACT_PATH}. OCR will fail for scanned PDFs.")

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "..", "uploads")
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

def allowed_file(name):
    return "." in name and name.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# UPLOAD DOCUMENT

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

        # Secure the filename to prevent directory traversal attacks
        original_filename = secure_filename(file.filename)
        ext = original_filename.rsplit(".", 1)[1].lower()
        
        # Generate unique path
        unique_name = f"{uuid.uuid4()}.{ext}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_name)
        file.save(file_path)

        new_doc = Document(
            user_id=user_id,
            doc_name=original_filename,
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
        logger.error(f"Upload Error: {e}")
        return {"status": "error", "message": str(e)}, 500



# PROCESS DOCUMENT (Route Handler)

def process_document(doc_id):
    try:
        doc = Document.query.get(doc_id)
        if not doc: return {"error": "Not found"}, 404

        if not doc.raw_text:
            text = extract_and_clean_text(doc.file_path)
            if not text: return {"error": "Extraction failed"}, 500
            doc.raw_text = text
            db.session.commit()

        results = process_document_by_id(doc_id)
        return {"status": "success", "data": results}, 200
    except Exception as e:
        return {"error": str(e)}, 500

def extract_and_clean_text(path):
    ext = path.split('.')[-1].lower()
    text = ""
    try:
        if ext == 'pdf':
            with fitz.open(path) as pdf:
                for page in pdf:
                    t = page.get_text()
                    if len(t) < 50: # OCR Fallback
                        try:
                            pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
                            img = Image.open(io.BytesIO(pix.tobytes("png")))
                            t = pytesseract.image_to_string(img)
                        except: pass
                    text += t + " "
        elif ext == 'txt':
            with open(path, 'r', encoding='utf-8') as f: text = f.read()
    except Exception as e:
        logger.error(f"Extract error: {e}")
        return ""

    # CLEANING
    text = re.sub(r'[|_\u2014\u2013]', ' ', text) # Remove artifacts
    text = re.sub(r'\s+', ' ', text).strip() # Normalize space
    return text