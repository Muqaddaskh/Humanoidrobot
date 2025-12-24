# RAG Configuration for PhysicalAI Humanoid Robotics Textbook

# Chunking Configuration
CHUNK_SIZE: int = 512  # Number of tokens per chunk
CHUNK_OVERLAP: int = 64  # Number of overlapping tokens between chunks
MIN_CHUNK_SIZE: int = 128  # Minimum size for a chunk to be considered

# Textbook-specific chunking rules
SEPARATOR_RULES: list = [
    "\n## ",  # New sections
    "\n### ",  # New subsections
    "\n\n",  # Paragraph breaks
    ". ",  # Sentence endings
    " ",  # Word boundaries (last resort)
]

# Content filtering rules
IGNORE_SECTIONS: list = [
    "References",
    "Further Reading",
    "Exercises",
    "About This Textbook"
]

# Metadata fields to preserve
METADATA_FIELDS: list = [
    "chapter",
    "section",
    "subsection",
    "page_number",
    "learning_objectives"
]

# Retrieval configuration
MAX_CONTEXTS_RETURNED: int = 5  # Maximum number of context chunks to return
MIN_RELEVANCE_SCORE: float = 0.5  # Minimum similarity score for inclusion