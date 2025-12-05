from documents.celery_app import celery_app
from documents.AI_model import process_text_full
from database.extensions import db
from database.dbmodels import Document, Summarization
import uuid
import traceback

@celery_app.task(name="process_document_task", bind=True)
def process_document_task(self, doc_id: str):
    try:
        from documents.doc_services import (
            extract_text_from_pdf, extract_text_from_docx,
            extract_text_from_txt, extract_tables_from_pdf
        )

        # Fetch document
        document = Document.query.get(doc_id)
        if not document:
            return {"status": "error", "message": "Document not found", "doc_id": doc_id}

        file_path = document.file_path
        if not file_path:
            return {"status": "error", "message": "Missing file_path", "doc_id": doc_id}

        # Detect extension + read text
        ext = file_path.lower().rsplit(".", 1)[-1]
        raw_text = ""
        tables = []

        if ext == "pdf":
            raw_text = extract_text_from_pdf(file_path)
            try:
                tables = extract_tables_from_pdf(file_path)
            except Exception:
                tables = []

        elif ext == "docx":
            raw_text = extract_text_from_docx(file_path)

        elif ext == "txt":
            raw_text = extract_text_from_txt(file_path)

        else:
            return {"status": "error", "message": f"Unsupported file type: {ext}", "doc_id": doc_id}

        # Run main NLP processing
        processed = process_text_full(raw_text)

        # NEW: properly extract summaries
        paragraph_blocks = processed.get("paragraphs", [])

        extracted_data = {
            "cleaned_text": processed.get("cleaned_text"),

            # paragraph + summary together
            "paragraphs": paragraph_blocks,

            # only summaries list
            "paragraph_summaries": [p.get("summary") for p in paragraph_blocks],

            # combined summary text
            "combined_summary": " ".join([p.get("summary") for p in paragraph_blocks]),

            "entities": processed.get("entities"),
            "tables": tables,

            # metadata
            "embeddings_meta": {
                "paragraph_count": len(processed.get("embeddings", []))
            }
        }

        # Save summarization result
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

        return {
            "status": "completed",
            "doc_id": doc_id,
            "summary_id": summary_record.summary_id,
        }

    except Exception as e:
        tb = traceback.format_exc()
        try:
            db.session.rollback()
        except:
            pass

        return {
            "status": "error",
            "doc_id": doc_id,
            "message": str(e),
            "traceback": tb
        }
