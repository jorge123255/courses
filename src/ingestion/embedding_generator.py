"""
Embedding generator module for creating and storing vector embeddings.
"""
import os
from typing import Dict, List, Any
from tqdm import tqdm
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import config


class EmbeddingGenerator:
    """
    Handles generation and storage of embeddings for text chunks.
    """
    
    def __init__(self, model_name: str = None, db_dir: str = None):
        """
        Initialize the embedding generator.
        
        Args:
            model_name: Name of the embedding model to use
            db_dir: Directory to store the vector database
        """
        self.model_name = model_name or config.EMBEDDING_MODEL
        self.db_dir = db_dir or config.DB_DIR
        
        # Initialize the embedding model
        self.model = SentenceTransformer(self.model_name)
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path=str(self.db_dir),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Create or get the collection
        self.collection = self.client.get_or_create_collection(
            name="cissp_knowledge",
            metadata={"hnsw:space": "cosine"}
        )
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            List of embedding vectors
        """
        return self.model.encode(texts, show_progress_bar=True).tolist()
    
    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        """
        Add documents to the vector database.
        
        Args:
            documents: List of dictionaries containing text and metadata
        """
        if not documents:
            print("No documents to add")
            return
        
        # Prepare data for ChromaDB
        ids = []
        texts = []
        metadatas = []
        
        for i, doc in enumerate(documents):
            doc_id = f"{doc['metadata'].get('title', 'unknown')}_{doc['metadata'].get('page_number', 0)}_{doc['metadata'].get('chunk_id', i)}"
            doc_id = doc_id.replace(" ", "_").replace("/", "_")
            
            ids.append(doc_id)
            texts.append(doc['text'])
            metadatas.append(doc['metadata'])
        
        # Add documents in batches to avoid memory issues
        batch_size = 100
        for i in tqdm(range(0, len(ids), batch_size), desc="Adding to database"):
            batch_end = min(i + batch_size, len(ids))
            
            batch_ids = ids[i:batch_end]
            batch_texts = texts[i:batch_end]
            batch_metadatas = metadatas[i:batch_end]
            
            # Generate embeddings for this batch
            batch_embeddings = self.generate_embeddings(batch_texts)
            
            # Add to ChromaDB
            self.collection.add(
                ids=batch_ids,
                embeddings=batch_embeddings,
                documents=batch_texts,
                metadatas=batch_metadatas
            )
        
        print(f"Added {len(ids)} documents to the database")
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the collection.
        
        Returns:
            Dictionary with collection statistics
        """
        count = self.collection.count()
        return {
            "count": count,
            "collection_name": self.collection.name
        }


if __name__ == "__main__":
    # Test the embedding generator
    from pdf_processor import PDFProcessor
    from text_chunker import TextChunker
    
    processor = PDFProcessor()
    chunker = TextChunker()
    embedding_generator = EmbeddingGenerator()
    
    pdf_files = processor.get_pdf_files()
    
    if pdf_files:
        test_pdf = pdf_files[0]
        print(f"Processing {test_pdf}")
        
        pdf_content = {
            "metadata": processor.extract_metadata(test_pdf),
            "text_by_page": processor.extract_text_from_pdf(test_pdf)
        }
        
        chunks = chunker.process_pdf_content(pdf_content)
        print(f"Created {len(chunks)} chunks")
        
        if chunks:
            embedding_generator.add_documents(chunks)
            stats = embedding_generator.get_collection_stats()
            print(f"Collection stats: {stats}")
