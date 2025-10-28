# RAG Tutor

RAG Tutor is a locally deployable Retrieval-Augmented Generation (RAG) based voice-enabled tutor that uses LangChain, Hugging Face, and FAISS to answer questions from your own documents — completely offline.  
It combines speech recognition, retrieval-based reasoning, and local language model inference to create an interactive tutoring experience.

---

## Features

- Voice Interaction — Speak your query; the AI listens and replies vocally.  
- RAG Pipeline — Retrieves relevant context from your local documents.  
- LLM-Powered Tutoring — Uses a lightweight summarization model (BART) for response generation.  
- Local FAISS Vector Store — No cloud dependency.  
- Emotion-Driven Mascot — Responds visually with expressive emotions.  
- FastAPI Backend + React Frontend — Modern, modular, and easily deployable.  
- Embeddings via HuggingFace — SentenceTransformer model for semantic similarity.  
- Fully Offline — Ideal for restricted environments or educational setups.

---

## Tech Stack

| Layer | Technology |
|-------|-------------|
| Frontend | React + TailwindCSS + SpeechSynthesis + Web Speech API |
| Backend | FastAPI |
| RAG Engine | LangChain + FAISS + Hugging Face Pipelines |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
| Model | facebook/bart-large-cnn |
| Environment | Python 3.10+, Node 18+ |

---

## Folder Structure

```
RAG Tutor/
│
├── backend/
│ ├── app/
│ │ ├── main.py # FastAPI app entry
│ │ ├── rag_engine.py # Core RAG logic
│ │ └── vectorstore/
│ │ ├── build_vectorstore.py # Script to build FAISS index
│ │ └── faiss_index/ # Stored vector database
│ ├── docs/ # Local text documents for RAG
│ └── venv/ # Virtual environment (Python)
│
├── frontend/
│ ├── public/ # Static assets
│ ├── src/
│ │ ├── components/
│ │ │ ├── Mascot.jsx # Voice mascot with speech + emotion
│ │ │ └── ChatWindow.jsx # Chat UI component
│ │ ├── App.js # Root app component
│ │ ├── index.js # Entry point
│ │ └── index.css # Styling
│ └── package.json # React dependencies
│
└── README.md

```

---

## Installation & Setup

### 1️. Backend Setup
cd backend
python -m venv venv
venv\Scriptsctivate # On Linux: source venv/bin/activate
pip install -r requirements.txt

text

Required dependencies:
fastapi
uvicorn
langchain
langchain-community
langchain-core
langchain-huggingface
faiss-cpu
transformers
sentence-transformers

text

### 2. Add Documents
Place your `.txt` files inside:
backend/docs/

text

Example:
backend/docs/intro.txt
backend/docs/langchain_overview.txt

text

### 3. Build the Vector Store
python backend/app/vectorstore/build_vectorstore.py

text

You should see:
FAISS index saved at: backend/app/vectorstore/faiss_index

text

### 4. Start Backend Server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

text

Access API docs at:  
http://127.0.0.1:8000/docs

Test API:
curl -X POST "http://127.0.0.1:8000/chat"
-H "Content-Type: application/json"
-d "{"query": "What is LangChain?"}"

text

### 5. Frontend Setup
cd frontend
npm install
npm start

text

Frontend runs at:  
http://localhost:3000

---

## API Schema

POST /chat

Request:
{
"query": "What is LangChain?"
}

text

Response:
{
"text": "LangChain is a framework for building applications powered by language models.",
"emotion": "explaining",
"sources": ["intro.txt"]
}

text

---

## Key Learnings & Challenges

### Problem Understanding
Building a self-contained AI tutor that interacts using voice and contextually reasons from local documents.

### Step-by-Step Breakdown
- Document ingestion → chunking → embedding → FAISS indexing  
- Query retrieval using semantic similarity  
- Local LLM (BART) for summarization-based generation  
- Voice input & synthesis integration in React  
- Emotion-driven mascot rendering  

### Key Decisions
- Used FAISS for fast offline similarity search.  
- Adopted HuggingFacePipeline for local LLM calls.  
- Simplified RAG logic for low-latency local inference.

### Challenges & Learnings
- Model compatibility fixed via HuggingFacePipeline.invoke  
- CORS and 422 schema mismatches resolved in FastAPI  

---

## 📘 License

MIT License © 2025 Gokul
