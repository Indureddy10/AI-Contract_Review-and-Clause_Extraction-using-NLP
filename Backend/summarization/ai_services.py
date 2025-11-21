from transformers import pipeline
import spacy
from spacy.pipeline import EntityRuler
import re
import json

# Load once (lazy)
_summarizer = None
_nlp = None

def _load_models():
    global _summarizer, _nlp
    if _summarizer is None:
        _summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    if _nlp is None:
        _nlp = spacy.load("en_core_web_sm")  # upgrade to transformer model if needed
        ruler = EntityRuler(_nlp, overwrite_ents=True)
        patterns = [
            {"label":"EFFECTIVE_DATE", "pattern":[{"LOWER":"effective"},{"LOWER":"date"}]},
            {"label":"INDEMNIFICATION", "pattern":[{"LOWER":"indemnification"}]},
            # add more patterns or load from JSONL
        ]
        ruler.add_patterns(patterns)
        _nlp.add_pipe(ruler, before="ner")

def clean_text(text: str) -> str:
    text = re.sub(r"\s+\n", "\n", text)
    text = re.sub(r"\n{2,}", "\n\n", text)
    return text.strip()

def summarize_text(text: str, max_length=200):
    _load_models()
    # chunk if long
    if len(text.split()) > 800:
        # naive: take first 800 words as representative for summary
        fragment = " ".join(text.split()[:800])
    else:
        fragment = text
    res = _summarizer(fragment, max_length=max_length, min_length=30, do_sample=False)
    return res[0]["summary_text"]

def extract_entities_and_clauses(text: str):
    _load_models()
    doc = _nlp(text)
    entities = []
    for ent in doc.ents:
        entities.append({"text": ent.text, "label": ent.label_, "start": ent.start_char, "end": ent.end_char})
    # Rule-based clause extraction examples (near keyword)
    clauses = []
    for sent in doc.sents:
        s = sent.text.lower()
        if "termination" in s or "terminate" in s:
            clauses.append({"type":"Termination","text":sent.text})
        if "indemnif" in s:
            clauses.append({"type":"Indemnification","text":sent.text})
    return {"entities": entities, "clauses": clauses}

def extract_document_ai(filepath: str):
    # 1. load text from file (pdf/docx) — reuse your parser
    from documents.parsers import extract_text_from_file
    raw_text = extract_text_from_file(filepath)
    raw_text = clean_text(raw_text)

    # 2. summarization
    summary = summarize_text(raw_text, max_length=200)

    # 3. spaCy extraction
    extractions = extract_entities_and_clauses(raw_text)

    return summary, extractions, raw_text
