import streamlit as st
from transformers import pipeline

@st.cache_resource
def load_qa_pipeline():
    return pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

qa_pipeline = load_qa_pipeline()

def answer_question(question: str, context: str) -> dict:
    if not question.strip():
        return {"answer": "❌ Question was empty", "score": 0, "start": 0, "end": 0}

    response = qa_pipeline(question=question, context=context)
    return {
        "answer": response["answer"],
        "score": response["score"],
        "start": response["start"],
        "end": response["end"]
    }
