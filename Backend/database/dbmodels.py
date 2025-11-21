"""
database/models.py

Defines all database models used in the project.
"""

from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from database.extensions import db
import sqlalchemy as sa
import uuid



class User(db.Model):
    __tablename__ = "authentication"

    user_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_name = db.Column(db.String(250), nullable=False)
    user_mail = db.Column(db.String(250), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    token = db.Column(db.Text)

     
    documents = db.relationship("Document", back_populates="authentication", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.user_mail}>"

    def to_dict(self):
        return {
            "user_id": str(self.user_id),
            "user_name": self.user_name,
            "user_mail": self.user_mail,
            "created_time": self.created_time.isoformat() if self.created_time else None,
        }
    
class Document(db.Model):
    __tablename__ = 'documents'

    doc_id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('authentication.user_id', ondelete='CASCADE'), nullable=False)
    doc_name = db.Column(db.String(255), nullable=False)
    doc_type = db.Column(db.String(100))
    doc_size = db.Column(db.Integer)
    file_path = db.Column(db.Text, nullable=False)
    storage_type = db.Column(db.String(50), default='local')
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    status = db.Column(db.String, default='Uploaded')
    raw_text = db.Column(db.Text)

    __table_args__ = (
        db.CheckConstraint("status IN ('Uploaded','Processing','Complete','Error')", name='documents_status_check'),
    )

    # Correct model reference
    authentication = db.relationship("User", back_populates="documents")

    def __repr__(self):
        return f"<Document {self.doc_name} ({self.doc_type})>"

    def to_dict(self):
        return {
            "doc_id": str(self.doc_id),
            "user_id": str(self.user_id),
            "doc_name": self.doc_name,
            "doc_type": self.doc_type,
            "doc_size": self.doc_size,
            "file_path": self.file_path,
            "storage_type": self.storage_type,
            "uploaded_at": self.uploaded_at.isoformat() if self.uploaded_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_active": self.is_active,
            "status": self.status,
            "raw_text": self.raw_text if self.raw_text else None,
        }


 


class Summarization(db.Model):
    __tablename__ = "summarization"

    summary_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("authentication.user_id", ondelete="CASCADE"), nullable=False)
    doc_id  = db.Column(db.UUID(as_uuid=True), db.ForeignKey("documents.doc_id", ondelete="CASCADE"), nullable=False)

    doc_name = db.Column(db.String(255), nullable=False)
    extracted_data = db.Column(JSONB)
    extracted_clauses = db.Column(JSONB)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="summaries", lazy=True)
    documents = db.relationship("Document", backref="summaries", lazy=True)

