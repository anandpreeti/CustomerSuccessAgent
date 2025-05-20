import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter
from agents import function_tool 

VECTOR_STORE_DIR = "data/vectorstore"

def init_vector_store(article_texts, metadatas=None):
    # Embed
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.create_documents(article_texts, metadatas=metadatas or [{} for _ in article_texts])
    
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(docs, embeddings)
    db.save_local(VECTOR_STORE_DIR)
    return db


def load_vector_store():
    embeddings = OpenAIEmbeddings()
    return FAISS.load_local(
        folder_path=VECTOR_STORE_DIR,
        embeddings=embeddings,
        allow_dangerous_deserialization=True
    )

vector_lookup_tool = function_tool(load_vector_store)    

def vector_store_exists():
    return os.path.exists(os.path.join(VECTOR_STORE_DIR, "index.faiss"))
