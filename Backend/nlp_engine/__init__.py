# nlp_engine/__init__.py
from .processor import process_document_by_id, process_text
from .model_loader import get_ner_pipeline, get_clause_pipeline

__all__ = [
    "process_document_by_id",
    "process_text",
    "get_ner_pipeline",
    "get_clause_pipeline",
]
