# PhysicalAI Textbook RAG Backend

This is the backend service for the PhysicalAI Humanoid Robotics Textbook AI assistant, implementing Retrieval Augmented Generation (RAG) to answer questions based strictly on textbook content.

## Features

- FastAPI-based REST API
- Qdrant vector store for content retrieval
- Textbook-specific chunking and embedding
- Strict RAG implementation ensuring answers come only from textbook content

## Dependencies

- Python 3.8+
- FastAPI
- Qdrant Client
- Transformers (for embeddings)
- PyTorch

## Setup

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. (Optional) Set up environment variables in a `.env` file:
   ```
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_api_key
   ```

## Running the Server

```bash
cd backend
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

## API Endpoints

### Health Check
- `GET /health` - Check if the service is running

### Question Answering
- `POST /ask` - Ask questions about textbook content
  ```json
  {
    "question": "What are the fundamentals of robotics?"
  }
  ```

### Content Ingestion
- `POST /ingest` - Add textbook content to the RAG system
  ```json
  {
    "content": "Textbook chapter content...",
    "metadata": {
      "chapter": "Chapter 1",
      "section": "Fundamentals"
    }
  }
  ```

### Content Search
- `GET /search` - Search for specific content in the textbook
  ```
  /search?query=kinematics&top_k=5
  ```

## Configuration

The RAG system can be configured via `rag_config.py`:

- `CHUNK_SIZE`: Number of tokens per content chunk
- `CHUNK_OVERLAP`: Overlap between chunks
- `MAX_CONTEXTS_RETURNED`: Maximum contexts to return for a query
- `MIN_RELEVANCE_SCORE`: Minimum similarity score for context inclusion

## Architecture

The backend follows this architecture:

1. **Document Processor**: Splits textbook content into semantically meaningful chunks
2. **Embedding Service**: Converts text to vector embeddings using transformer models
3. **Vector Store**: Stores embeddings in Qdrant for efficient similarity search
4. **RAG Service**: Orchestrates the retrieval and generation process
5. **API Layer**: FastAPI endpoints for frontend integration

## Deployment

For production deployment:

1. Use a proper WSGI/ASGI server like Gunicorn
2. Set up a persistent Qdrant instance (cloud or self-hosted)
3. Configure proper authentication and rate limiting
4. Set up monitoring and logging

Example production command:
```bash
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker
```