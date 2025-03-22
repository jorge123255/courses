"""
Configuration settings for the CISSP Tutor & Exam Platform.
"""
import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = PROJECT_ROOT / "data"
PDF_DIR = DATA_DIR / "pdfs"
DB_DIR = DATA_DIR / "vectordb"

# Create directories if they don't exist
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(DB_DIR, exist_ok=True)

# Embedding settings
EMBEDDING_MODEL = "BAAI/bge-large-en"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# Retrieval settings
TOP_K = 5
SIMILARITY_THRESHOLD = 0.75  # Threshold for contradiction detection

# LLM settings
LLM_MODEL = "llama3.1:8b"  # Model to use with Ollama
OLLAMA_BASE_URL = "http://localhost:11434"

# Tutoring settings
MAX_HISTORY_LENGTH = 10  # Number of previous interactions to maintain in context
