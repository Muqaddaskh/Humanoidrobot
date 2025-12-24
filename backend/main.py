from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

import rag_service
import embedding_service
import vector_store

app = FastAPI(title="PhysicalAI Textbook RAG API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str
    context_filter: Dict[str, Any] = {}

class DocumentRequest(BaseModel):
    content: str
    metadata: Dict[str, Any]

class AnswerResponse(BaseModel):
    answer: str
    contexts: List[Dict[str, Any]]
    confidence: float

@app.get("/")
def read_root():
    return {"message": "PhysicalAI Textbook RAG API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest):
    """
    Answer a question based on the textbook content using RAG
    """
    try:
        result = rag_service.rag_service.answer_question(request.question)
        return AnswerResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest")
def ingest_document(request: DocumentRequest):
    """
    Ingest a document into the RAG system
    """
    try:
        success = rag_service.rag_service.ingest_document(request.content, request.metadata)
        if success:
            return {"message": "Document ingested successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to ingest document")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search")
def search_content(query: str, top_k: int = 5):
    """
    Search for content in the textbook
    """
    try:
        # Generate embedding for the query
        query_embedding = embedding_service.embedding_service.generate_embedding(query)

        # Search in vector store
        results = vector_store.vector_store.search(query_embedding, top_k=top_k)

        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))