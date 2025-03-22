"""
LLM interface module for interacting with Ollama.
"""
import os
import json
import requests
from typing import Dict, List, Any, Optional

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import config


class OllamaInterface:
    """
    Interface for interacting with Ollama LLM.
    """
    
    def __init__(self, model_name: str = None, base_url: str = None):
        """
        Initialize the Ollama interface.
        
        Args:
            model_name: Name of the LLM model to use
            base_url: Base URL for the Ollama API
        """
        self.model_name = model_name or config.LLM_MODEL
        self.base_url = base_url or config.OLLAMA_BASE_URL
        self.api_url = f"{self.base_url}/api/generate"
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None, 
                 temperature: float = 0.7, max_tokens: int = 2048) -> str:
        """
        Generate a response from the LLM.
        
        Args:
            prompt: User prompt
            system_prompt: System prompt for the LLM
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Generated text response
        """
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        try:
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "")
        except requests.exceptions.RequestException as e:
            print(f"Error generating response: {e}")
            return f"Error: Could not generate response. Please ensure Ollama is running with the {self.model_name} model loaded."
    
    def is_available(self) -> bool:
        """
        Check if Ollama is available.
        
        Returns:
            True if Ollama is available, False otherwise
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException:
            return False


class RAGPromptBuilder:
    """
    Builds prompts for RAG-based question answering.
    """
    
    @staticmethod
    def build_qa_prompt(query: str, context: str, include_sources: bool = True) -> str:
        """
        Build a prompt for question answering with RAG.
        
        Args:
            query: User query
            context: Retrieved context
            include_sources: Whether to include source citations in the response
            
        Returns:
            Formatted prompt for the LLM
        """
        source_instruction = ""
        if include_sources:
            source_instruction = (
                "Include source citations in your answer by referencing the numbers in square brackets. "
                "For example, 'According to [1], ...' or 'Sources [1] and [2] state that...'"
            )
        
        prompt = f"""
I need information about the following CISSP-related question:

{query}

Here is relevant information from CISSP study materials:

{context}

Based on the information provided above, please answer the question thoroughly.
{source_instruction}
If the information provided doesn't fully answer the question, acknowledge what isn't covered.
If there are contradictions in the sources, explicitly point them out and explain the different perspectives.
"""
        return prompt
    
    @staticmethod
    def build_contradiction_prompt(query: str, contradictions: Dict[str, Any]) -> str:
        """
        Build a prompt for explaining contradictions.
        
        Args:
            query: User query
            contradictions: Contradiction information
            
        Returns:
            Formatted prompt for the LLM
        """
        contradiction_texts = []
        
        for i, contradiction in enumerate(contradictions.get("contradictions", [])):
            doc1 = contradiction["doc1"]
            doc2 = contradiction["doc2"]
            similarity = contradiction["similarity"]
            
            source1 = f"{doc1['metadata'].get('title', 'Unknown')}, Page {doc1['metadata'].get('page_number', 'N/A')}"
            source2 = f"{doc2['metadata'].get('title', 'Unknown')}, Page {doc2['metadata'].get('page_number', 'N/A')}"
            
            contradiction_texts.append(f"""
Contradiction {i+1} (Similarity: {similarity:.2f}):

Source A ({source1}):
{doc1['text']}

Source B ({source2}):
{doc2['text']}
""")
        
        contradiction_text = "\n".join(contradiction_texts)
        
        prompt = f"""
I found potential contradictions in the CISSP study materials when answering this question:

{query}

Here are the contradicting passages:

{contradiction_text}

Please analyze these contradictions and explain:
1. What specific information is contradictory
2. Why these contradictions might exist (different perspectives, standards, or contexts)
3. Which interpretation is more likely correct in the context of CISSP certification
4. How a CISSP professional should understand this topic considering these different viewpoints
"""
        return prompt
    
    @staticmethod
    def build_system_prompt() -> str:
        """
        Build a system prompt for the LLM.
        
        Returns:
            System prompt
        """
        return """
You are a CISSP (Certified Information Systems Security Professional) tutor and expert. 
Your role is to provide accurate, clear, and comprehensive explanations of CISSP concepts 
based on authoritative sources. Always cite your sources when providing information.

When explaining concepts:
- Be precise and technically accurate
- Provide practical examples where appropriate
- Highlight key points for CISSP exam preparation
- Acknowledge when information might be incomplete or contradictory
- Maintain a professional, educational tone

Your goal is to help the user understand CISSP concepts deeply, not just memorize facts.
"""


if __name__ == "__main__":
    # Test the Ollama interface
    ollama = OllamaInterface()
    
    if not ollama.is_available():
        print("Ollama is not available. Please ensure it is running.")
    else:
        print("Ollama is available.")
        
        # Test with a simple prompt
        system_prompt = RAGPromptBuilder.build_system_prompt()
        test_prompt = "What is the CIA triad in information security?"
        
        print(f"Generating response for: {test_prompt}")
        response = ollama.generate(test_prompt, system_prompt)
        
        print("\nResponse:")
        print(response)
