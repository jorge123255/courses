"""
Module for processing EPUB files and extracting text content.
"""
import os
from pathlib import Path
from typing import List, Tuple, Dict, Any
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class EPUBProcessor:
    """
    Class for processing EPUB files and extracting text content.
    """
    
    def __init__(self, epub_dir: str = None):
        """
        Initialize the EPUB processor.
        
        Args:
            epub_dir: Directory containing EPUB files
        """
        self.epub_dir = Path(epub_dir) if epub_dir else None
    
    def process_all_epubs(self, epub_dir: str = None) -> List[Dict[str, Any]]:
        """
        Process all EPUB files in the specified directory.
        
        Args:
            epub_dir: Directory containing EPUB files
            
        Returns:
            List of dictionaries with extracted text and metadata
        """
        if epub_dir:
            self.epub_dir = Path(epub_dir)
        
        if not self.epub_dir or not self.epub_dir.exists():
            logger.error(f"EPUB directory does not exist: {self.epub_dir}")
            return []
        
        results = []
        for file_path in self.epub_dir.glob("**/*.epub"):
            try:
                logger.info(f"Processing EPUB: {file_path}")
                epub_data = self.process_epub(file_path)
                results.append(epub_data)
            except Exception as e:
                logger.error(f"Error processing EPUB {file_path}: {e}")
        
        return results
    
    def process_epub(self, epub_path: Path) -> Dict[str, Any]:
        """
        Process a single EPUB file and extract text and metadata.
        
        Args:
            epub_path: Path to the EPUB file
            
        Returns:
            Dictionary with extracted text and metadata
        """
        book = epub.read_epub(str(epub_path))
        
        # Extract metadata
        metadata = self._extract_metadata(book)
        
        # Extract text content
        content = self._extract_text_content(book)
        
        return {
            "file_path": str(epub_path),
            "file_name": epub_path.name,
            "metadata": metadata,
            "content": content
        }
    
    def _extract_metadata(self, book: epub.EpubBook) -> Dict[str, Any]:
        """
        Extract metadata from an EPUB book.
        
        Args:
            book: EpubBook object
            
        Returns:
            Dictionary with metadata
        """
        metadata = {}
        
        # Get title
        metadata["title"] = book.get_metadata('DC', 'title')
        
        # Get creator/author
        metadata["author"] = book.get_metadata('DC', 'creator')
        
        # Get language
        metadata["language"] = book.get_metadata('DC', 'language')
        
        # Get publisher
        metadata["publisher"] = book.get_metadata('DC', 'publisher')
        
        # Get publication date
        metadata["date"] = book.get_metadata('DC', 'date')
        
        # Get description
        metadata["description"] = book.get_metadata('DC', 'description')
        
        # Get identifier
        metadata["identifier"] = book.get_metadata('DC', 'identifier')
        
        # Clean up metadata (extract values from lists)
        for key, value in metadata.items():
            if isinstance(value, list) and len(value) > 0:
                # Extract the first value if it's a list
                if isinstance(value[0], tuple) and len(value[0]) > 0:
                    metadata[key] = value[0][0]
                else:
                    metadata[key] = value[0]
            elif not value:
                metadata[key] = None
        
        return metadata
    
    def _extract_text_content(self, book: epub.EpubBook) -> List[Tuple[int, str]]:
        """
        Extract text content from an EPUB book.
        
        Args:
            book: EpubBook object
            
        Returns:
            List of tuples (chapter_index, text_content)
        """
        chapters = []
        chapter_index = 0
        
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                try:
                    # Get HTML content
                    html_content = item.get_content().decode('utf-8')
                    
                    # Parse HTML with BeautifulSoup
                    soup = BeautifulSoup(html_content, 'html.parser')
                    
                    # Extract text (remove script and style elements)
                    for script in soup(["script", "style"]):
                        script.extract()
                    
                    # Get text
                    text = soup.get_text(separator=' ')
                    
                    # Clean up text
                    lines = (line.strip() for line in text.splitlines())
                    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                    text = ' '.join(chunk for chunk in chunks if chunk)
                    
                    if text.strip():  # Only add non-empty chapters
                        chapters.append((chapter_index, text))
                        chapter_index += 1
                except Exception as e:
                    logger.error(f"Error processing chapter: {e}")
        
        return chapters
    
    def extract_text_from_epub(self, epub_path: Path) -> List[Tuple[int, str]]:
        """
        Extract text from an EPUB file.
        
        Args:
            epub_path: Path to the EPUB file
            
        Returns:
            List of tuples (chapter_index, text_content)
        """
        try:
            book = epub.read_epub(str(epub_path))
            return self._extract_text_content(book)
        except Exception as e:
            logger.error(f"Error extracting text from EPUB {epub_path}: {e}")
            return []
