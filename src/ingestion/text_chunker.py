"""
Text chunking module for splitting extracted text into semantic units.
"""
import os
import re
from typing import Dict, List, Tuple, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import config


class TextChunker:
    """
    Handles chunking of text into semantic units for embedding.
    """
    
    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        """
        Initialize the text chunker.
        
        Args:
            chunk_size: Size of each chunk in tokens
            chunk_overlap: Overlap between chunks in tokens
        """
        self.chunk_size = chunk_size or config.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or config.CHUNK_OVERLAP
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def create_chunks(self, text: str, metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Split text into chunks with metadata.
        
        Args:
            text: Text to split into chunks
            metadata: Metadata to include with each chunk
            
        Returns:
            List of dictionaries containing text chunks and metadata
        """
        if not text:
            return []
        
        # Clean the text
        text = self._clean_text(text)
        
        # Split the text into chunks
        chunks = self.text_splitter.split_text(text)
        
        # Create documents with metadata
        documents = []
        for i, chunk in enumerate(chunks):
            chunk_metadata = metadata.copy() if metadata else {}
            chunk_metadata.update({
                "chunk_id": i,
                "chunk_count": len(chunks)
            })
            
            documents.append({
                "text": chunk,
                "metadata": chunk_metadata
            })
        
        return documents
    
    def process_document_content(self, document_content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Process the content of a document (PDF or EPUB) and create chunks with metadata.
        
        Args:
            document_content: Dictionary containing metadata and text by page/chapter
            
        Returns:
            List of dictionaries containing text chunks and metadata
        """
        metadata = document_content.get("metadata", {})
        text_by_section = document_content.get("text_by_page", [])  # Works for both PDFs and EPUBs
        source_type = document_content.get("source_type", "unknown")
        file_path = document_content.get("file_path", "")
        
        # Add file path to metadata
        if file_path:
            metadata["file_path"] = file_path
        
        all_chunks = []
        for section_num, section_text in text_by_section:
            section_metadata = metadata.copy()
            
            # Add appropriate metadata based on document type
            if source_type == "pdf":
                section_metadata.update({
                    "page_number": section_num,
                    "source_type": "pdf"
                })
            elif source_type == "epub":
                section_metadata.update({
                    "chapter_number": section_num,
                    "source_type": "epub"
                })
            else:
                section_metadata.update({
                    "section_number": section_num,
                    "source_type": source_type
                })
            
            chunks = self.create_chunks(section_text, section_metadata)
            all_chunks.extend(chunks)
        
        return all_chunks
        
    def process_pdf_content(self, pdf_content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Process the content of a PDF and create chunks with metadata (legacy method).
        
        Args:
            pdf_content: Dictionary containing metadata and text by page
            
        Returns:
            List of dictionaries containing text chunks and metadata
        """
        # Add source type if not present
        if "source_type" not in pdf_content:
            pdf_content["source_type"] = "pdf"
            
        return self.process_document_content(pdf_content)
    
    def _clean_text(self, text: str) -> str:
        """
        Clean text before chunking.
        
        Args:
            text: Text to clean
            
        Returns:
            Cleaned text
        """
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove headers, footers, and page numbers (simplified approach)
        text = re.sub(r'\d+\s*$', '', text)  # Remove standalone page numbers
        
        return text.strip()


if __name__ == "__main__":
    # Test the text chunker
    from pdf_processor import PDFProcessor
    from epub_processor import EPUBProcessor
    import os
    from pathlib import Path
    
    # Test with PDF
    print("\nTesting with PDF:")
    pdf_processor = PDFProcessor()
    pdf_files = pdf_processor.get_pdf_files()
    
    if pdf_files:
        test_pdf = pdf_files[0]
        print(f"Processing {test_pdf}")
        
        pdf_content = {
            "metadata": pdf_processor.extract_metadata(test_pdf),
            "text_by_page": pdf_processor.extract_text_from_pdf(test_pdf),
            "source_type": "pdf",
            "file_path": str(test_pdf)
        }
        
        chunker = TextChunker()
        chunks = chunker.process_document_content(pdf_content)
        
        print(f"Created {len(chunks)} chunks")
        if chunks:
            print(f"Sample chunk:")
            print(f"Text: {chunks[0]['text'][:100]}...")
            print(f"Metadata: {chunks[0]['metadata']}")
    
    # Test with EPUB if available
    print("\nTesting with EPUB:")
    epub_dir = config.PDF_DIR  # Reusing the same directory
    epub_processor = EPUBProcessor(epub_dir)
    epub_files = list(Path(epub_dir).glob("**/*.epub"))
    
    if epub_files:
        test_epub = epub_files[0]
        print(f"Processing {test_epub}")
        
        try:
            epub_data = epub_processor.process_epub(test_epub)
            
            epub_content = {
                "metadata": epub_data['metadata'],
                "text_by_page": epub_data['content'],
                "source_type": "epub",
                "file_path": str(test_epub)
            }
            
            chunker = TextChunker()
            chunks = chunker.process_document_content(epub_content)
            
            print(f"Created {len(chunks)} chunks")
            if chunks:
                print(f"Sample chunk:")
                print(f"Text: {chunks[0]['text'][:100]}...")
                print(f"Metadata: {chunks[0]['metadata']}")
        except Exception as e:
            print(f"Error processing EPUB: {e}")
    else:
        print("No EPUB files found for testing")
