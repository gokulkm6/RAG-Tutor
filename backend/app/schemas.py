from pydantic import BaseModel
from typing import Optional, List

class QueryRequest(BaseModel):
    query: str

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str

class RAGResponse(BaseModel):
    text: str
    emotion: Optional[str] = "neutral"
    sources: Optional[List[str]] = []