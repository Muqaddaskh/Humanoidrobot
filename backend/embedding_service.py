from typing import List
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch

class EmbeddingService:
    """
    Service for generating text embeddings using transformer models
    """

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize the embedding service with a pre-trained model
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.model.eval()  # Set to evaluation mode

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        """
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)

        with torch.no_grad():
            outputs = self.model(**inputs)
            # Use mean pooling to get the sentence embedding
            embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

        # Normalize the embedding
        embedding = embedding / np.linalg.norm(embedding)
        return embedding.tolist()

    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a batch of texts
        """
        embeddings = []
        for text in texts:
            embeddings.append(self.generate_embedding(text))
        return embeddings

# Singleton instance
embedding_service = EmbeddingService()