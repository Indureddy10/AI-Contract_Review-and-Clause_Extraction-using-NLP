import os
import logging
from transformers import AutoTokenizer, AutoModelForTokenClassification, AutoModelForSeq2SeqLM, pipeline

LOGGER = logging.getLogger(__name__)

# CONFIGURATION
DEFAULT_NER_MODEL = "dslim/bert-base-NER"
DEFAULT_SUMM_MODEL = "sshleifer/distilbart-cnn-12-6"
DEFAULT_CLAUSE_MODEL = "facebook/bart-large-mnli" # Zero-Shot

_ner_pipeline = None
_summ_pipeline = None
_clause_pipeline = None

def get_device():
    return 0 if os.getenv("USE_CUDA") else -1

def get_ner_pipeline():
    global _ner_pipeline
    if _ner_pipeline: return _ner_pipeline
    LOGGER.info(f"Loading NER: {DEFAULT_NER_MODEL}")
    try:
        tokenizer = AutoTokenizer.from_pretrained(DEFAULT_NER_MODEL)
        model = AutoModelForTokenClassification.from_pretrained(DEFAULT_NER_MODEL)
        _ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple", device=get_device())
        return _ner_pipeline
    except Exception as e:
        LOGGER.error(f"NER Load Error: {e}")
        return None

def get_summarization_pipeline():
    global _summ_pipeline
    if _summ_pipeline: return _summ_pipeline
    LOGGER.info(f"Loading Summarizer: {DEFAULT_SUMM_MODEL}")
    try:
        tokenizer = AutoTokenizer.from_pretrained(DEFAULT_SUMM_MODEL)
        model = AutoModelForSeq2SeqLM.from_pretrained(DEFAULT_SUMM_MODEL)
        _summ_pipeline = pipeline("summarization", model=model, tokenizer=tokenizer, device=get_device())
        return _summ_pipeline
    except Exception as e:
        LOGGER.error(f"Summarizer Load Error: {e}")
        return None

def get_clause_pipeline():
    global _clause_pipeline
    if _clause_pipeline: return _clause_pipeline
    LOGGER.info(f"Loading Clause Classifier: {DEFAULT_CLAUSE_MODEL}")
    try:
        _clause_pipeline = pipeline("zero-shot-classification", model=DEFAULT_CLAUSE_MODEL, device=get_device())
        return _clause_pipeline
    except Exception as e:
        LOGGER.error(f"Clause Model Load Error: {e}")
        return None