from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def evaluate_answer(user_answer: str, document: str) -> str:
    # Break document into sentences
    from nltk.tokenize import sent_tokenize
    doc_sentences = sent_tokenize(document)

    # Embed user answer and all document sentences
    user_embedding = model.encode(user_answer, convert_to_tensor=True)
    doc_embeddings = model.encode(doc_sentences, convert_to_tensor=True)

    # Compute similarity
    similarities = util.pytorch_cos_sim(user_embedding, doc_embeddings)[0]
    max_sim = float(similarities.max())

    if max_sim > 0.6:
        matched_sentence = doc_sentences[int(similarities.argmax())]
        return f"✅ Match found. Closest sentence: *{matched_sentence}* (Score: {round(max_sim, 2)})"
    else:
        return "❌ No strong semantic match in the document."
