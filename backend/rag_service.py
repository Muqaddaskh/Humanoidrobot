from typing import List, Dict, Any
from .vector_store import vector_store
from .embedding_service import embedding_service
from .document_processor import document_processor
from .rag_config import MAX_CONTEXTS_RETURNED

class RAGService:
    """
    Main RAG service that handles document ingestion and question answering
    """

    def __init__(self):
        self.vector_store = vector_store
        self.embedding_service = embedding_service
        self.document_processor = document_processor

    def ingest_document(self, content: str, metadata: Dict[str, Any]) -> bool:
        """
        Ingest a document into the RAG system
        """
        try:
            # Process the document into chunks
            chunks = self.document_processor.chunk_textbook_content(content, metadata)

            # Generate embeddings for each chunk and store in vector store
            for chunk in chunks:
                embedding = self.embedding_service.generate_embedding(chunk["content"])
                self.vector_store.add_document(chunk["content"], chunk["metadata"])

            return True
        except Exception as e:
            print(f"Error ingesting document: {str(e)}")
            return False

    def answer_question(self, question: str) -> Dict[str, Any]:
        """
        Answer a question using the RAG system
        """
        try:
            # Generate embedding for the question
            question_embedding = self.embedding_service.generate_embedding(question)

            # Retrieve relevant contexts from vector store
            contexts = self.vector_store.search(question_embedding, top_k=MAX_CONTEXTS_RETURNED)

            if not contexts:
                return {
                    "answer": "I couldn't find relevant information in the textbook to answer your question.",
                    "contexts": [],
                    "confidence": 0.0
                }

            # Combine contexts to form the answer
            context_texts = [ctx["content"] for ctx in contexts]
            combined_context = " ".join(context_texts)

            # In a real implementation, we would use an LLM to generate the answer based on contexts
            # For this implementation, we'll return the most relevant context as the answer
            answer = self._generate_answer(question, combined_context, contexts)

            return {
                "answer": answer,
                "contexts": contexts,
                "confidence": max([ctx["score"] for ctx in contexts]) if contexts else 0.0
            }
        except Exception as e:
            print(f"Error answering question: {str(e)}")
            return {
                "answer": "An error occurred while processing your question.",
                "contexts": [],
                "confidence": 0.0
            }

    def _generate_answer(self, question: str, context: str, contexts: List[Dict[str, Any]]) -> str:
        """
        Generate an answer based on the question and retrieved contexts
        """
        # In a real implementation, this would call an LLM to generate a response
        # For now, we'll return a simple response based on the most relevant context
        if contexts:
            best_context = max(contexts, key=lambda x: x["score"])
            return f"Based on the textbook: {best_context['content']}"
        else:
            return "I couldn't find relevant information in the textbook to answer your question."

# Singleton instance
rag_service = RAGService()