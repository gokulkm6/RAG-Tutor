import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import FAISS

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
DOCS_FOLDER = "backend/docs"
PERSIST_DIR = "backend/app/vectorstore/faiss_index"

def ingest_docs(folder=DOCS_FOLDER, persist_directory=PERSIST_DIR):
    if not os.path.exists(folder):
        raise FileNotFoundError(f"Docs folder not found: {folder}. Create and add .txt files.")

    docs = []
    for fname in os.listdir(folder):
        if fname.lower().endswith(".txt"):
            path = os.path.join(folder, fname)
            loader = TextLoader(path, encoding="utf-8")
            docs.extend(loader.load())

    if not docs:
        raise ValueError("No .txt documents found in docs folder.")

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    split_docs = splitter.split_documents(docs)

    embeddings = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    vectordb = FAISS.from_documents(split_docs, embeddings)

    os.makedirs(persist_directory, exist_ok=True)
    vectordb.save_local(persist_directory)
    print("FAISS index saved at:", persist_directory)

if __name__ == "__main__":
    ingest_docs()
