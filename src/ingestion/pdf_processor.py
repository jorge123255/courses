"""
PDF processing module for extracting text from CISSP study materials.
"""
import os
import fitz  # PyMuPDF
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import re
from tqdm import tqdm

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import config


class PDFProcessor:
    """
    Handles extraction of text from PDF files.
    """
    
    def __init__(self, pdf_dir: Optional[Path] = None):
        """
        Initialize the PDF processor.
        
        Args:
            pdf_dir: Directory containing PDF files to process
        """
        self.pdf_dir = pdf_dir or config.PDF_DIR
        os.makedirs(self.pdf_dir, exist_ok=True)
    
    def get_pdf_files(self) -> List[Path]:
        """
        Get all PDF files in the configured directory.
        
        Returns:
            List of paths to PDF files
        """
        return list(self.pdf_dir.glob("*.pdf"))
    
    def extract_metadata(self, pdf_path: Path) -> Dict[str, str]:
        """
        Extract metadata from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary containing metadata (title, author, etc.)
        """
        try:
            doc = fitz.open(pdf_path)
            metadata = doc.metadata
            
            # Clean up metadata
            result = {
                "title": metadata.get("title", "") or pdf_path.stem,
                "author": metadata.get("author", "Unknown"),
                "subject": metadata.get("subject", ""),
                "keywords": metadata.get("keywords", ""),
                "file_path": str(pdf_path),
                "page_count": len(doc)
            }
            
            doc.close()
            return result
        except Exception as e:
            print(f"Error extracting metadata from {pdf_path}: {e}")
            return {
                "title": pdf_path.stem,
                "author": "Unknown",
                "file_path": str(pdf_path),
                "page_count": 0
            }
    
    def extract_text_from_pdf(self, pdf_path: Path) -> List[Tuple[int, str]]:
        """
        Extract text from a PDF file, page by page.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of tuples containing (page_number, text)
        """
        try:
            doc = fitz.open(pdf_path)
            text_by_page = []
            
            for page_num, page in enumerate(doc):
                text = page.get_text()
                # Clean up text
                text = re.sub(r'\s+', ' ', text)
                text = text.strip()
                
                if text:  # Only add non-empty pages
                    text_by_page.append((page_num + 1, text))
            
            doc.close()
            return text_by_page
        except Exception as e:
            print(f"Error extracting text from {pdf_path}: {e}")
            return []
    
    def process_all_pdfs(self) -> Dict[str, Dict]:
        """
        Process all PDFs in the directory and extract text and metadata.
        
        Returns:
            Dictionary mapping file paths to dictionaries containing metadata and text
        """
        pdf_files = self.get_pdf_files()
        if not pdf_files:
            print(f"No PDF files found in {self.pdf_dir}")
            return {}
        
        results = {}
        for pdf_path in tqdm(pdf_files, desc="Processing PDFs"):
            metadata = self.extract_metadata(pdf_path)
            text_by_page = self.extract_text_from_pdf(pdf_path)
            
            results[str(pdf_path)] = {
                "metadata": metadata,
                "text_by_page": text_by_page
            }
        
        return results


if __name__ == "__main__":
    # Test the PDF processor
    processor = PDFProcessor()
    pdf_files = processor.get_pdf_files()
    print(f"Found {len(pdf_files)} PDF files")
    
    if pdf_files:
        test_pdf = pdf_files[0]
        print(f"Processing {test_pdf}")
        metadata = processor.extract_metadata(test_pdf)
        print(f"Metadata: {metadata}")
        
        text_by_page = processor.extract_text_from_pdf(test_pdf)
        print(f"Extracted {len(text_by_page)} pages with text")
        if text_by_page:
            print(f"Sample from page {text_by_page[0][0]}:")
            print(text_by_page[0][1][:200] + "...")
