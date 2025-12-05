"""
database/models.py
"""

from datetime import datetime
import uuid
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB
from database.extensions import db

class User(db.Model):
    __tablename__ = "authentication"

    user_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_name = db.Column(db.String(250), nullable=False)
    user_mail = db.Column(db.String(250), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    token = db.Column(db.Text)
    
    # Relationships
    documents = db.relationship("Document", back_populates="authentication", cascade="all, delete-orphan")
    summaries = db.relationship("Summarization", backref="user", lazy=True)

    def to_dict(self):
        return {
            "user_id": str(self.user_id),
            "user_name": self.user_name,
            "user_mail": self.user_mail
        }

class Document(db.Model):
    __tablename__ = 'documents'

    doc_id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(db.String(36), db.ForeignKey('authentication.user_id', ondelete='CASCADE'), nullable=False)
    
    doc_name = db.Column(db.String(255), nullable=False)
    doc_type = db.Column(db.String(100))
    doc_size = db.Column(db.Integer)
    file_path = db.Column(db.Text, nullable=False)
    storage_type = db.Column(db.String(50), default='local')
    
    # Status tracking
    status = db.Column(db.String(50), default='Uploaded') 
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # THIS STORES THE CLEANED ORIGINAL DATA
    # We strip out OCR noise before saving here.
    raw_text = db.Column(db.Text) 

    # Relationships
    authentication = db.relationship("User", back_populates="documents")
    summaries = db.relationship("Summarization", backref="document", cascade="all, delete-orphan", lazy=True)

    def to_dict(self):
        return {
            "doc_id": str(self.doc_id),
            "doc_name": self.doc_name,
            "status": self.status,
            "uploaded_at": self.uploaded_at.isoformat() if self.uploaded_at else None,
            "has_text": bool(self.raw_text) # Helper for frontend
        }

class Summarization(db.Model):
    __tablename__ = "summarization"

    summary_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign Keys
    user_id = db.Column(db.String(36), db.ForeignKey("authentication.user_id", ondelete="CASCADE"), nullable=False)
    doc_id  = db.Column(db.UUID(as_uuid=True), db.ForeignKey("documents.doc_id", ondelete="CASCADE"), nullable=False)
    doc_name = db.Column(db.String(255), nullable=False)

    # --- NEW FIELDS REQUESTED ---
    
    # 1. SUMMARY TABLE (Paragraphs or Points)
    summary_text = db.Column(db.Text) 

    # 2. EXTRACTED CLAUSES (JSON Format)
    # Structure: {"termination": ["..."], "liability": ["..."], "dates": ["..."]}
    extracted_clauses = db.Column(JSONB) 

    # 3. CONTRACT REVIEW (Text)
    # Stores the overall analysis or risk review
    contract_review = db.Column(db.Text)
    
    # Optional: Keep entities if you still need them (Names, Orgs)
    extracted_entities = db.Column(JSONB) 

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "summary_id": self.summary_id,
            "doc_id": str(self.doc_id),
            "summary_text": self.summary_text,
            "extracted_clauses": self.extracted_clauses,
            "contract_review": self.contract_review,
            "extracted_entities": self.extracted_entities,
            "created_at": self.created_at.isoformat()
        }