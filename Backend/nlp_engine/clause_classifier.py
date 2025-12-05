import re
from typing import Dict, List
from .model_loader import get_clause_pipeline

def classify_clauses(text: str) -> Dict[str, List[str]]:
    """
    Classifies sentences into legal categories using Zero-Shot Learning.
    """
    labels = ["Termination", "Indemnification", "Confidentiality", "Payment Terms", "Governing Law"]
    clauses = {k.lower().split()[0]: [] for k in labels} # keys: termination, indemnification...
    
    if not text: return clauses

    clf = get_clause_pipeline()
    if not clf: return clauses

    # 1. Pre-filter sentences (Optimization)
    # Running Zero-Shot on 50 pages is too slow. We filter sentences containing keywords first, 
    # THEN verify them with the AI model.
    keywords = ["terminat", "cancel", "indemnif", "harmless", "confident", "disclos", "payment", "invoice", "law", "jurisdiction"]
    
    # Split sentences roughly
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text.replace('\n', ' '))
    candidates = [s.strip() for s in sentences if len(s) > 50 and any(k in s.lower() for k in keywords)]

    # Limit to top 30 candidates for performance
    candidates = candidates[:30]

    if not candidates: return clauses

    # 2. Run Transformer
    try:
        results = clf(candidates, labels, multi_label=False)
        for res in results:
            score = res['scores'][0]
            label = res['labels'][0]
            sentence = res['sequence']
            
            # High confidence threshold
            if score > 0.55:
                key = label.lower().split()[0] # Map 'Termination Clause' -> 'termination'
                if key in clauses:
                    clauses[key].append(sentence)
    except Exception as e:
        print(f"Clause Classification Error: {e}")

    return clauses