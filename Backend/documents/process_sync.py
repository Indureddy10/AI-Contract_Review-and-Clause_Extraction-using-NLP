# documents/process_sync.py

from documents.AI_model import process_text_full
from documents.doc_services import extract_text
from database.extensions import db
from database.dbmodels import Document, Summarization
import uuid
import traceback


def process_document_sync(doc_id: str):
    try:
        document = Document.query.get(doc_id)
        if not document:
            return {"status": "error", "message": "Document not found"}

        raw_text = extract_text(document.file_path)
        processed = process_text_full(raw_text)

        paragraph_blocks = processed.get("paragraphs", [])

        extracted_data = {
            "cleaned_text": processed.get("cleaned_text"),
            "paragraphs": paragraph_blocks,
            "paragraph_summaries": [p["summary"] for p in paragraph_blocks],
            "combined_summary": " ".join([p["summary"] for p in paragraph_blocks]),
            "entities": processed.get("entities")
        }

        summary_record = Summarization(
            summary_id=str(uuid.uuid4()),
            user_id=document.user_id,
            doc_id=document.doc_id,
            doc_name=document.doc_name,
            extracted_data=extracted_data,
            extracted_clauses=processed.get("clauses"),
        )

        db.session.add(summary_record)
        db.session.commit()

        return {"status": "completed", "summary_id": summary_record.summary_id}

    except Exception as e:
        db.session.rollback()
        return {"status": "error", "message": str(e), "trace": traceback.format_exc()}
