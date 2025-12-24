from typing import List, Dict, Any, Optional
import uuid
from qdrant_client import QdrantClient
from qdrant_client.http import models
from .rag_config import MAX_CONTEXTS_RETURNED, MIN_RELEVANCE_SCORE

class VectorStore:
    """
    Handles vector storage and retrieval for the RAG system
    """

    def __init__(self, collection_name: str = "textbook_content"):
        # Initialize Qdrant client (assuming local instance or cloud)
        self.client = QdrantClient(":memory:")  # Using in-memory for now, can be changed to actual server
        self.collection_name = collection_name
        self._create_collection()

    def _create_collection(self):
        """
        Create the collection for storing textbook content vectors
        """
        try:
            # Check if collection already exists
            self.client.get_collection(self.collection_name)
        except:
            # Create collection if it doesn't exist
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=1536,  # Size for OpenAI embeddings
                    distance=models.Distance.COSINE
                )
            )

    def add_document(self, content: str, metadata: Dict[str, Any]) -> str:
        """
        Add a document chunk to the vector store
        """
        # In a real implementation, we would generate embeddings here
        # For now, we'll use a placeholder
        vector_id = str(uuid.uuid4())

        # Placeholder for embedding generation
        # In reality, you'd use OpenAI, SentenceTransformers, or similar
        embedding = [0.0] * 1536  # Placeholder embedding

        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=vector_id,
                    vector=embedding,
                    payload={
                        "content": content,
                        "metadata": metadata
                    }
                )
            ]
        )

        return vector_id

    def search(self, query_embedding: List[float], top_k: int = MAX_CONTEXTS_RETURNED) -> List[Dict[str, Any]]:
        """
        Search for relevant content based on query embedding
        """
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=top_k,
            score_threshold=MIN_RELEVANCE_SCORE
        )

        return [
            {
                "content": result.payload["content"],
                "metadata": result.payload["metadata"],
                "score": result.score
            }
            for result in results
            if result.score >= MIN_RELEVANCE_SCORE
        ]

    def add_documents_batch(self, chunks: List[Dict[str, Any]]) -> List[str]:
        """
        Add multiple document chunks in batch
        """
        vector_ids = []
        for chunk in chunks:
            vector_id = self.add_document(chunk["content"], chunk["metadata"])
            vector_ids.append(vector_id)
        return vector_ids

# Singleton instance
vector_store = VectorStore()