from langchain.tools import Tool
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings

VECTOR_STORE_PATH = "data/vectorstore"

def query_knowledge_base(query: str) -> str:
    embeddings = OpenAIEmbeddings()
    db = FAISS.load_local(VECTOR_STORE_PATH, embeddings)
    docs = db.similarity_search(query, k=3)
    if not docs:
        return "No relevant information found."
    
    return "\n\n".join([doc.page_content for doc in docs])

knowledge_base_tool = Tool(
    name="KnowledgeBase",
    func=query_knowledge_base,
    description="Useful for answering questions from the Zendesk knowledge base or internal documentation."
)
