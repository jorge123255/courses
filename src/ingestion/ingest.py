"""
Main ingestion script for processing PDF and EPUB files and generating embeddings.
"""
import os
import argparse
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple
from tqdm import tqdm

from .pdf_processor import PDFProcessor
from .epub_processor import EPUBProcessor
from .text_chunker import TextChunker
from .embedding_generator import EmbeddingGenerator

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import config


def ingest_documents(doc_dir: Optional[Path] = None, force_reindex: bool = False, file_types: List[str] = None):
    """
    Process all documents (PDFs and EPUBs) in the directory and generate embeddings.
    
    Args:
        doc_dir: Directory containing document files to process
        force_reindex: Whether to force reindexing of all documents
        file_types: List of file types to process (e.g., ['pdf', 'epub'])
    """
    if doc_dir is None:
        doc_dir = config.PDF_DIR
    
    if file_types is None:
        file_types = ['pdf', 'epub']
    
    # Initialize components
    pdf_processor = PDFProcessor(doc_dir)
    epub_processor = EPUBProcessor(doc_dir)
    chunker = TextChunker()
    embedding_generator = EmbeddingGenerator()
    
    # Process PDFs if requested
    if 'pdf' in file_types:
        process_pdfs(pdf_processor, chunker, embedding_generator, force_reindex)
    
    # Process EPUBs if requested
    if 'epub' in file_types:
        process_epubs(epub_processor, chunker, embedding_generator, force_reindex)
    
    # Print final stats
    stats = embedding_generator.get_collection_stats()
    print(f"\nIngestion complete. Collection stats: {stats}")


def process_pdfs(processor: PDFProcessor, chunker: TextChunker, 
                embedding_generator: EmbeddingGenerator, force_reindex: bool = False):
    """
    Process all PDFs using the provided processor.
    
    Args:
        processor: PDFProcessor instance
        chunker: TextChunker instance
        embedding_generator: EmbeddingGenerator instance
        force_reindex: Whether to force reindexing
    """
    # Get PDF files
    pdf_files = processor.get_pdf_files()
    if not pdf_files:
        print(f"No PDF files found in {processor.pdf_dir}")
        return
    
    print(f"Found {len(pdf_files)} PDF files")
    
    # Process each PDF
    for pdf_path in tqdm(pdf_files, desc="Processing PDFs"):
        print(f"\nProcessing {pdf_path}")
        
        # Extract metadata and text
        metadata = processor.extract_metadata(pdf_path)
        text_by_page = processor.extract_text_from_pdf(pdf_path)
        
        pdf_content = {
            "metadata": metadata,
            "text_by_page": text_by_page,
            "source_type": "pdf",
            "file_path": str(pdf_path)
        }
        
        # Create chunks
        chunks = chunker.process_document_content(pdf_content)
        print(f"Created {len(chunks)} chunks")
        
        # Generate and store embeddings
        if chunks:
            embedding_generator.add_documents(chunks)


def process_epubs(processor: EPUBProcessor, chunker: TextChunker, 
                 embedding_generator: EmbeddingGenerator, force_reindex: bool = False):
    """
    Process all EPUBs using the provided processor.
    
    Args:
        processor: EPUBProcessor instance
        chunker: TextChunker instance
        embedding_generator: EmbeddingGenerator instance
        force_reindex: Whether to force reindexing
    """
    # Get EPUB files
    epub_files = list(processor.epub_dir.glob("**/*.epub"))
    if not epub_files:
        print(f"No EPUB files found in {processor.epub_dir}")
        return
    
    print(f"Found {len(epub_files)} EPUB files")
    
    # Process each EPUB
    for epub_path in tqdm(epub_files, desc="Processing EPUBs"):
        print(f"\nProcessing {epub_path}")
        
        try:
            # Extract text and metadata
            epub_data = processor.process_epub(epub_path)
            
            # Format content similar to PDF for chunker
            text_by_chapter = epub_data['content']
            
            epub_content = {
                "metadata": epub_data['metadata'],
                "text_by_page": text_by_chapter,  # Using the same field name for consistency
                "source_type": "epub",
                "file_path": str(epub_path)
            }
            
            # Create chunks
            chunks = chunker.process_document_content(epub_content)
            print(f"Created {len(chunks)} chunks")
            
            # Generate and store embeddings
            if chunks:
                embedding_generator.add_documents(chunks)
                
        except Exception as e:
            print(f"Error processing EPUB {epub_path}: {e}")


def ingest_pdfs(pdf_dir: Optional[Path] = None, force_reindex: bool = False):
    """
    Legacy function for backwards compatibility.
    
    Args:
        pdf_dir: Directory containing PDF files to process
        force_reindex: Whether to force reindexing of all PDFs
    """
    ingest_documents(pdf_dir, force_reindex, file_types=['pdf'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest document files and generate embeddings")
    parser.add_argument("--doc_dir", type=str, help="Directory containing document files")
    parser.add_argument("--force", action="store_true", help="Force reindexing of all documents")
    parser.add_argument("--file_types", type=str, nargs="+", default=["pdf", "epub"], 
                        choices=["pdf", "epub"], help="File types to process")
    
    args = parser.parse_args()
    
    doc_dir = Path(args.doc_dir) if args.doc_dir else None
    ingest_documents(doc_dir, args.force, args.file_types)
