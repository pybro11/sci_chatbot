# papers/utils.py
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text):
    summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
    return summary[0]['summary_text']

# papers/utils.py
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_texts(texts):
    return model.encode(texts)

def setup_faiss_index(embedded_texts):
    dimension = embedded_texts.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embedded_texts)
    return index

def search_similar_papers(query_text, index, paper_texts, top_k=5):
    query_embedding = model.encode([query_text])
    distances, indices = index.search(query_embedding, top_k)
    return [paper_texts[i] for i in indices[0]]
