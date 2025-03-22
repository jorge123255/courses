# CISSP Tutor & Exam Platform

An intelligent tutoring system for CISSP exam preparation using embeddings and RAG (Retrieval Augmented Generation).

## Features

- Document ingestion and knowledge extraction (PDF and EPUB formats)
- Intelligent question answering with source citations
- Contradiction detection across multiple sources
- Adaptive learning and personalized recommendations
- Exam simulation with multiple-choice questions
- Progress tracking and performance analytics
- Command-line and web interfaces

## Quick Setup

The easiest way to get started is to use the setup script:

```bash
python setup.py
```

This script will:
1. Check your system requirements (RAM, disk space, GPU availability)
2. Install dependencies
3. Verify Ollama installation and model availability
4. Download sample CISSP study materials
5. Process and index the materials

### Manual Setup

If you prefer to set up manually:

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Ollama for local LLM support: https://ollama.ai/
```bash
# Pull the required model
ollama pull llama3.1:8b
```

3. Download sample materials:
```bash
python download_samples.py
```

4. Process the materials:
```bash
# Process all document types (PDF and EPUB)
python -m src.ingestion.ingest --file_types pdf epub

# Or process specific document types
python -m src.ingestion.ingest --file_types pdf  # PDFs only
python -m src.ingestion.ingest --file_types epub  # EPUBs only
```

5. Run the application:
```bash
python run_app.py
```

## Project Structure

- `data/` - Directory for storing document files (PDF and EPUB)
- `db/` - Vector database and embeddings storage
- `src/` - Source code
  - `ingestion/` - Document processing and embedding generation
    - `pdf_processor.py` - PDF processing module
    - `epub_processor.py` - EPUB processing module
    - `text_chunker.py` - Text chunking for both formats
    - `embedding_generator.py` - Vector embedding generation
  - `retrieval/` - RAG implementation and context retrieval
  - `tutoring/` - Q&A and adaptive learning system
  - `exam/` - Exam simulation and grading
- `app.py` - Streamlit web application
- `cli.py` - Command-line interface
- `run_app.py` - Script to run the web application
- `setup.py` - Setup and configuration script
- `download_samples.py` - Script to download sample CISSP materials
- `config.py` - Configuration settings

## Usage

### Web Interface

Start the web interface:

```bash
python run_app.py
```

This will launch a Streamlit app with the following features:
- Document upload and processing (PDF and EPUB formats)
- Interactive Q&A with the CISSP tutor
- Exam generation and taking
- Performance analytics

### Command-Line Interface

The CLI provides access to core functionality:

```bash
# Ask a question
python cli.py ask "What is the CIA triad?"

# Generate an exam
python cli.py exam --count 20 --output exam.json

# Take an exam
python cli.py take exam.json

# Ingest new documents
python cli.py ingest --doc_dir /path/to/docs --file_types pdf epub
```

## System Requirements

### Minimum Requirements
- Python 3.11+
- Ollama (for local LLM access)
- 8GB RAM
- 2GB disk space for embeddings and model cache
- CPU with AVX2 instruction support

### Recommended Requirements
- 16GB+ RAM
- NVIDIA GPU with 8GB+ VRAM (for faster inference)
- AMD GPU with ROCm support
- Apple Silicon (M1/M2/M3) for optimized performance on Mac
- 5GB+ disk space

### Model-Specific Requirements
- **Llama 3.1 8B**: 
  - CPU-only: 16GB RAM recommended
  - GPU: 8GB+ VRAM
  - Disk: ~4GB for model storage

> **Note**: Ollama automatically detects and utilizes available GPUs. Performance will vary based on your hardware. The setup script will check your system and provide guidance.

## License

[MIT License](LICENSE)
