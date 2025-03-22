"""
Retrieval module for finding relevant context from the vector database.
"""
import os
from typing import Dict, List, Any, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from sklearn.metrics.pairwise import cosine_similarity

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import config


class Retriever:
    """
    Handles retrieval of relevant context from the vector database.
    """
    
    def __init__(self, model_name: str = None, db_dir: str = None, top_k: int = None):
        """
        Initialize the retriever.
        
        Args:
            model_name: Name of the embedding model to use
            db_dir: Directory containing the vector database
            top_k: Number of results to retrieve
        """
        self.model_name = model_name or config.EMBEDDING_MODEL
        self.db_dir = db_dir or config.DB_DIR
        self.top_k = top_k or config.TOP_K
        
        # Initialize the embedding model
        self.model = SentenceTransformer(self.model_name)
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path=str(self.db_dir),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get the collection
        try:
            self.collection = self.client.get_collection("cissp_knowledge")
            print(f"Connected to collection with {self.collection.count()} documents")
        except ValueError:
            print("Collection not found. Please run the ingestion process first.")
            self.collection = None
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate an embedding for a single text.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        return self.model.encode(text).tolist()
    
    def retrieve(self, query: str, top_k: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a query.
        
        Args:
            query: Query text
            top_k: Number of results to retrieve (overrides instance setting)
            
        Returns:
            List of dictionaries containing retrieved documents and metadata
        """
        if not self.collection:
            print("Collection not available. Please run the ingestion process first.")
            return []
        
        k = top_k or self.top_k
        
        # Generate embedding for the query
        query_embedding = self.generate_embedding(query)
        
        # Query the collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            include=["documents", "metadatas", "distances"]
        )
        
        # Format the results
        formatted_results = []
        for i in range(len(results["documents"][0])):
            formatted_results.append({
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i]
            })
        
        return formatted_results
    
    def detect_contradictions(self, results: List[Dict[str, Any]], threshold: float = None) -> Dict[str, Any]:
        """
        Detect contradictions in retrieved results.
        
        Args:
            results: List of retrieved documents
            threshold: Similarity threshold for contradiction detection
            
        Returns:
            Dictionary with contradiction information
        """
        if not results or len(results) < 2:
            return {"has_contradictions": False, "contradictions": []}
        
        threshold = threshold or config.SIMILARITY_THRESHOLD
        
        # Extract texts and generate embeddings
        texts = [result["text"] for result in results]
        embeddings = [self.generate_embedding(text) for text in texts]
        
        # Compute pairwise similarities
        similarities = cosine_similarity(embeddings)
        
        # Find potential contradictions (low similarity)
        contradictions = []
        for i in range(len(results)):
            for j in range(i + 1, len(results)):
                similarity = similarities[i][j]
                
                if similarity < threshold:
                    contradictions.append({
                        "doc1": {
                            "text": results[i]["text"],
                            "metadata": results[i]["metadata"]
                        },
                        "doc2": {
                            "text": results[j]["text"],
                            "metadata": results[j]["metadata"]
                        },
                        "similarity": float(similarity)
                    })
        
        return {
            "has_contradictions": len(contradictions) > 0,
            "contradictions": contradictions
        }
    
    def format_context(self, results: List[Dict[str, Any]], include_metadata: bool = True) -> str:
        """
        Format retrieved results into a context string for the LLM.
        
        Args:
            results: List of retrieved documents
            include_metadata: Whether to include metadata in the context
            
        Returns:
            Formatted context string
        """
        if not results:
            return "No relevant information found."
        
        context_parts = []
        
        for i, result in enumerate(results):
            text = result["text"]
            metadata = result["metadata"]
            
            if include_metadata:
                source = f"{metadata.get('title', 'Unknown Source')}"
                page = metadata.get('page_number', 'N/A')
                context_parts.append(f"[{i+1}] From: {source}, Page: {page}\n{text}\n")
            else:
                context_parts.append(f"[{i+1}] {text}\n")
        
        return "\n".join(context_parts)


if __name__ == "__main__":
    # Test the retriever
    retriever = Retriever()
    
    test_query = "What are the key components of the CIA triad?"
    print(f"Query: {test_query}")
    
    results = retriever.retrieve(test_query)
    print(f"Retrieved {len(results)} documents")
    
    if results:
        print("\nSample result:")
        print(f"Text: {results[0]['text'][:200]}...")
        print(f"Metadata: {results[0]['metadata']}")
        print(f"Distance: {results[0]['distance']}")
        
        # Test contradiction detection
        contradictions = retriever.detect_contradictions(results)
        print(f"\nContradictions detected: {contradictions['has_contradictions']}")
        if contradictions['has_contradictions']:
            print(f"Found {len(contradictions['contradictions'])} contradictions")
        
        # Test context formatting
        context = retriever.format_context(results)
        print("\nFormatted context:")
        print(context)
