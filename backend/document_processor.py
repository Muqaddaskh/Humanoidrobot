import re
from typing import List, Dict, Any
from .rag_config import CHUNK_SIZE, CHUNK_OVERLAP, SEPARATOR_RULES, IGNORE_SECTIONS, METADATA_FIELDS

class DocumentProcessor:
    """
    Processes textbook documents for RAG system, handling chunking and preprocessing
    """

    def __init__(self):
        self.chunk_size = CHUNK_SIZE
        self.chunk_overlap = CHUNK_OVERLAP

    def chunk_textbook_content(self, text: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Chunk textbook content according to defined rules
        """
        chunks = []

        # Remove ignored sections
        text = self._remove_ignored_sections(text)

        # Split content based on separator rules
        for separator in SEPARATOR_RULES:
            if len(text) <= self.chunk_size:
                break
            chunks = self._split_by_separator(text, separator, metadata)
            if chunks:
                break

        # If no chunks were created with separators, split by length
        if not chunks:
            chunks = self._split_by_length(text, metadata)

        return chunks

    def _remove_ignored_sections(self, text: str) -> str:
        """
        Remove sections that should not be included in the RAG system
        """
        for section in IGNORE_SECTIONS:
            pattern = f"## {section}.*?(?=## |$)"
            text = re.sub(pattern, "", text, flags=re.DOTALL)
        return text

    def _split_by_separator(self, text: str, separator: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Split text by a specific separator
        """
        chunks = []
        parts = text.split(separator)

        current_chunk = ""
        for i, part in enumerate(parts):
            # Add separator back to all but the first part
            if i > 0:
                part = separator + part

            if len(current_chunk) + len(part) <= self.chunk_size:
                current_chunk += part
            else:
                if current_chunk.strip():
                    chunks.append({
                        "content": current_chunk.strip(),
                        "metadata": metadata.copy()
                    })
                    # Add overlap from the previous chunk
                    overlap_start = max(0, len(current_chunk) - self.chunk_overlap)
                    current_chunk = current_chunk[overlap_start:] + part
                else:
                    current_chunk = part

        if current_chunk.strip():
            chunks.append({
                "content": current_chunk.strip(),
                "metadata": metadata.copy()
            })

        return chunks

    def _split_by_length(self, text: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Split text by length when other methods fail
        """
        chunks = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size
            if end > len(text):
                end = len(text)

            chunk = text[start:end]
            chunks.append({
                "content": chunk.strip(),
                "metadata": metadata.copy()
            })

            start = end - self.chunk_overlap

        return chunks

# Singleton instance
document_processor = DocumentProcessor()