import re
from typing import Dict, List
from .model_loader import get_ner_pipeline

def extract_entities(text: str) -> Dict[str, List[str]]:
    if not text: return {}
    
    # 1. BERT Extraction (Limit text length for speed)
    ner = get_ner_pipeline()
    raw_entities = []
    if ner:
        try:
            raw_entities = ner(text[:10000])
        except: pass

    formatted = {
        "organizations": list(set([e['word'] for e in raw_entities if e['entity_group'] == 'ORG'])),
        "people": list(set([e['word'] for e in raw_entities if e['entity_group'] == 'PER'])),
        "locations": list(set([e['word'] for e in raw_entities if e['entity_group'] == 'LOC'])),
        "effective_dates": []
    }

    # 2. Regex for Dates (Fallback)
    # Catches: "November 25, 2025", "2025-11-25", "Effective Date: ..."
    date_patterns = [
        r'(?:Effective|Agreement)\s+Date[:\s]+([A-Z][a-z]+\s+\d{1,2},?\s+\d{4})',
        r'\d{4}-\d{2}-\d{2}',
        r'[A-Z][a-z]+\s\d{1,2},?\s\d{4}'
    ]
    
    found_dates = []
    for p in date_patterns:
        matches = re.findall(p, text, re.IGNORECASE)
        found_dates.extend(matches)
        
    formatted["effective_dates"] = list(set(found_dates))
    return formatted