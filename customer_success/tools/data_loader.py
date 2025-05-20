import os
import requests
from bs4 import BeautifulSoup

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document


# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = "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"


def get_zendesk_article_text(article_id):
    url = f"https://support.eventlogic.se/api/v2/help_center/articles/{article_id}.json"
    headers = {
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    data = response.json()
    raw_html = data["article"]["body"]
    soup = BeautifulSoup(raw_html, "html.parser")
    clean_text = soup.get_text(separator="\n", strip=True)
    return clean_text


def create_faiss_index_from_articles(article_ids, index_path="faiss_zendesk_index"):
    texts = []
    metadatas = []

    for article_id in article_ids:
        try:
            text = get_zendesk_article_text(article_id)
            texts.append(text)
            metadatas.append({"article_id": article_id})
        except Exception as e:
            print(f"Failed to fetch article {article_id}: {e}")

    # Split text
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.create_documents(texts, metadatas=metadatas)

    # Embed and store in FAISS
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(docs, embeddings)
    db.save_local(index_path)
    print(f"Saved FAISS index to: {index_path}")


# create_faiss_index_from_articles(["4410160179345"])
