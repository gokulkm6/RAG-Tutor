from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import QueryRequest, ChatRequest, RAGResponse
from app.rag_engine import answer_query_offline, infer_emotion
import uuid
import traceback

app = FastAPI(title="RAG Tutor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sessions = {}

@app.post("/query", response_model=RAGResponse)
async def query(payload: QueryRequest):
    try:
        answer, sources = answer_query_offline(payload.query)
        print(">>> QUERY:", payload.query)
        print(">>> ANSWER:", answer)
        emotion = infer_emotion(answer)
        return {"text": answer, "emotion": emotion, "sources": sources}
    except Exception as e:
        print(">>> ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=RAGResponse)
async def chat(request: QueryRequest):
    try:
        answer = answer_query_offline(request.query)
        emotion = infer_emotion(answer)
        return {"text": answer, "emotion": emotion, "sources": []}
    except Exception as e:
        print("❌ ERROR in /chat:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))