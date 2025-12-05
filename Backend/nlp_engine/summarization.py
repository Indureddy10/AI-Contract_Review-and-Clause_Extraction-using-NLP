from .model_loader import get_summarization_pipeline

def generate_chunked_summary(text: str) -> str:
    if not text: return ""
    summ_pipe = get_summarization_pipeline()
    if not summ_pipe: return ""

    clean_text = text.replace("\n", " ")
    chunk_size = 3000
    chunks = [clean_text[i:i+chunk_size] for i in range(0, len(clean_text), chunk_size)]
    
    summaries = []
    # Summarize Intro (Chunk 0) and Key Terms (Chunk 1)
    for i, chunk in enumerate(chunks[:2]):
        try:
            max_len = 150 if i == 0 else 100
            res = summ_pipe(chunk, max_length=max_len, min_length=40, do_sample=False)
            summaries.append(res[0]['summary_text'])
        except: continue

    return "\n\n".join(summaries)