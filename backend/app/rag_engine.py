from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline

def build_vectorstore(doc_path="docs/intro.txt", persist_path="app/vectorstore/faiss_index"):
    loader = TextLoader(doc_path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = FAISS.from_documents(chunks, embedder)
    vectordb.save_local(persist_path)
    return vectordb


def load_vectorstore(persist_path="app/vectorstore/faiss_index"):
    embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = FAISS.load_local(persist_path, embedder, allow_dangerous_deserialization=True)
    return vectordb


def get_llm():
    hf = pipeline("text2text-generation", model="facebook/bart-large-cnn")
    return HuggingFacePipeline(pipeline=hf)


def answer_query_offline(query: str):
    vectordb = load_vectorstore()
    llm = get_llm()
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})

    docs = retriever.invoke(query)
    context = "\n\n".join([d.page_content for d in docs])
    prompt = f"Answer the question based on the context below:\n\n{context}\n\nQuestion: {query}\nAnswer:"

    response = llm.invoke(prompt)

    if isinstance(response, list) and len(response) > 0:
        return response[0]['generated_text']
    elif hasattr(response, 'content'):
        return response.content
    else:
        return str(response)


def infer_emotion(response_text: str):
    if any(w in response_text.lower() for w in ["great", "good", "excellent"]):
        return "happy"
    elif "?" in response_text:
        return "thinking"
    return "explaining"


if __name__ == "__main__":
    print(answer_query_offline("What is LangChain?"))