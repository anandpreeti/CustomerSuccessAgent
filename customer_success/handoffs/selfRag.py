import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

import streamlit as st

def crawl_site(url, max_pages=10):
    visited = set()
    to_visit = [url]
    all_texts = []

    while to_visit and len(visited) < max_pages:
        current = to_visit.pop()
        if current in visited:
            continue
        try:
            response = requests.get(current)
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            all_texts.append((current, text))

            for link in soup.find_all('a', href=True):
                new_url = urljoin(current, link['href'])
                if url in new_url and new_url not in visited:
                    to_visit.append(new_url)
            visited.add(current)
        except Exception as e:
            print(f"Failed to fetch {current}: {e}")
    return all_texts


def clean_and_chunk(text, chunk_size=500):
    paragraphs = text.split('\n')
    chunks = []
    current = ""
    for para in paragraphs:
        if len(current) + len(para) < chunk_size:
            current += para + "\n"
        else:
            chunks.append(current)
            current = para
    if current:
        chunks.append(current)
    return chunks





def create_vector_store(pages):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    all_chunks = []
    urls = []
    for url, text in pages:
        chunks = clean_and_chunk(text)
        all_chunks.extend(chunks)
        urls.extend([url]*len(chunks))

    embeddings = model.encode(all_chunks)
    index = faiss.IndexFlatL2(384)
    index.add(np.array(embeddings))

    metadata = dict(enumerate(zip(urls, all_chunks)))
    return index, metadata


def retrieve(query, index, metadata, model=model, k=3):
    query_vector = model.encode([query])
    D, I = index.search(np.array(query_vector), k)
    return [metadata[i][1] for i in I[0]]  # return the text chunks


st.title("Self-RAG Web Crawler")
url = st.text_input("Enter URL to crawl")
query = st.text_input("Ask a question")

if st.button("Crawl and Index"):
    pages = crawl_site(url)
    index, metadata = create_vector_store(pages)
    st.success("Indexed!")

if st.button("Ask"):
    answers = retrieve(query, index, metadata)
    st.write("Answer context:")
    for a in answers:
        st.markdown(a)

