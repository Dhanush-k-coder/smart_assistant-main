from transformers import pipeline

# Load summarization model once (memoized for performance)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text: str, max_tokens=150) -> str:
    # Limit input length for summarization models
    text = text[:2000]
    result = summarizer(text, max_length=max_tokens, min_length=50, do_sample=False)
    return result[0]["summary_text"]
