from typing import Dict, Any
import logging
from .entity_extractor import extract_entities
from .clause_classifier import classify_clauses
from .summarization import generate_chunked_summary
from .contract_review import analyze_contract_risks
from database.models import Document, Summarization
from database.extensions import db

LOGGER = logging.getLogger(__name__)

def process_text(text: str) -> Dict[str, Any]:
    if not text: return {}

    # 1. Entities
    entities = extract_entities(text)
    
    # 2. Clauses (AI Classifiers)
    clauses = classify_clauses(text)
    
    # 3. Summary
    summary = generate_chunked_summary(text)
    
    # 4. Review
    review = analyze_contract_risks(clauses, entities, text)
    
    return {
        "entities": entities,
        "clauses": clauses,
        "summary": summary,
        "review": review
    }

def process_document_by_id(doc_id: str):
    doc = Document.query.get(doc_id)
    if not doc or not doc.raw_text: raise ValueError("Document not found/empty")

    try:
        doc.status = "Processing"
        db.session.commit()

        results = process_text(doc.raw_text)

        summary = Summarization(
            user_id=str(doc.user_id),
            doc_id=doc.doc_id,
            doc_name=doc.doc_name,
            summary_text=results["summary"],
            extracted_clauses=results["clauses"],
            extracted_entities=results["entities"],
            contract_review=results["review"]
        )
        
        db.session.add(summary)
        doc.status = "Complete"
        db.session.commit()
        return results["entities"]

    except Exception as e:
        LOGGER.exception(f"Processing failed: {doc_id}")
        db.session.rollback()
        doc.status = "Error"
        db.session.commit()
        raise