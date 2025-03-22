"""
Tutoring system module for interactive Q&A and adaptive learning.
"""
import os
import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import config
from src.retrieval.retriever import Retriever
from src.retrieval.llm_interface import OllamaInterface, RAGPromptBuilder


class UserSession:
    """
    Manages user session data and interaction history.
    """
    
    def __init__(self, user_id: str):
        """
        Initialize a user session.
        
        Args:
            user_id: Unique identifier for the user
        """
        self.user_id = user_id
        self.session_id = f"{user_id}_{int(time.time())}"
        self.interaction_history = []
        self.topic_strengths = {}  # Track user's understanding of topics
        self.last_active = datetime.now()
    
    def add_interaction(self, query: str, response: str, metadata: Dict[str, Any] = None) -> None:
        """
        Add an interaction to the history.
        
        Args:
            query: User query
            response: System response
            metadata: Additional metadata about the interaction
        """
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "response": response,
            "metadata": metadata or {}
        }
        
        self.interaction_history.append(interaction)
        self.last_active = datetime.now()
    
    def get_recent_interactions(self, count: int = None) -> List[Dict[str, Any]]:
        """
        Get recent interactions from the history.
        
        Args:
            count: Number of recent interactions to retrieve
            
        Returns:
            List of recent interactions
        """
        count = count or config.MAX_HISTORY_LENGTH
        return self.interaction_history[-count:] if self.interaction_history else []
    
    def update_topic_strength(self, topic: str, score: float) -> None:
        """
        Update the user's strength in a topic.
        
        Args:
            topic: Topic name
            score: Score indicating strength (0.0 to 1.0)
        """
        self.topic_strengths[topic] = score
    
    def get_weak_topics(self, threshold: float = 0.7) -> List[str]:
        """
        Get topics where the user's strength is below the threshold.
        
        Args:
            threshold: Strength threshold
            
        Returns:
            List of weak topics
        """
        return [topic for topic, strength in self.topic_strengths.items() if strength < threshold]
    
    def save_to_file(self, directory: str = None) -> str:
        """
        Save the session to a file.
        
        Args:
            directory: Directory to save the file in
            
        Returns:
            Path to the saved file
        """
        directory = directory or os.path.join(config.DATA_DIR, "sessions")
        os.makedirs(directory, exist_ok=True)
        
        filename = f"{self.session_id}.json"
        filepath = os.path.join(directory, filename)
        
        with open(filepath, 'w') as f:
            json.dump({
                "user_id": self.user_id,
                "session_id": self.session_id,
                "last_active": self.last_active.isoformat(),
                "interaction_history": self.interaction_history,
                "topic_strengths": self.topic_strengths
            }, f, indent=2)
        
        return filepath
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'UserSession':
        """
        Load a session from a file.
        
        Args:
            filepath: Path to the session file
            
        Returns:
            Loaded UserSession object
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        session = cls(data["user_id"])
        session.session_id = data["session_id"]
        session.interaction_history = data["interaction_history"]
        session.topic_strengths = data["topic_strengths"]
        session.last_active = datetime.fromisoformat(data["last_active"])
        
        return session


class AdaptiveLearning:
    """
    Manages adaptive learning features.
    """
    
    @staticmethod
    def analyze_query(query: str) -> Dict[str, Any]:
        """
        Analyze a query to identify topics and complexity.
        
        Args:
            query: User query
            
        Returns:
            Dictionary with analysis results
        """
        # This is a placeholder for more sophisticated analysis
        # In a real implementation, this would use NLP to identify topics
        
        # CISSP domains
        domains = [
            "Security and Risk Management",
            "Asset Security",
            "Security Architecture and Engineering",
            "Communication and Network Security",
            "Identity and Access Management",
            "Security Assessment and Testing",
            "Security Operations",
            "Software Development Security"
        ]
        
        # Simple keyword matching for domains
        identified_domains = []
        for domain in domains:
            if any(keyword.lower() in query.lower() for keyword in domain.split()):
                identified_domains.append(domain)
        
        # Estimate complexity based on query length and structure
        complexity = min(1.0, len(query.split()) / 20)  # Simple heuristic
        
        return {
            "topics": identified_domains,
            "complexity": complexity,
            "timestamp": datetime.now().isoformat()
        }
    
    @staticmethod
    def generate_follow_up_questions(query: str, response: str, llm: OllamaInterface) -> List[str]:
        """
        Generate follow-up questions based on the query and response.
        
        Args:
            query: User query
            response: System response
            llm: LLM interface for generating questions
            
        Returns:
            List of follow-up questions
        """
        prompt = f"""
Based on this question and answer about CISSP concepts:

Question: {query}

Answer: {response}

Generate 3 follow-up questions that would help deepen understanding of this topic. 
The questions should be progressively more advanced and help explore related concepts.
Format your response as a JSON array of strings, each containing one question.
"""
        
        system_prompt = "You are a CISSP tutor generating follow-up questions to deepen understanding."
        
        try:
            result = llm.generate(prompt, system_prompt, temperature=0.7)
            
            # Try to parse as JSON
            try:
                questions = json.loads(result)
                if isinstance(questions, list):
                    return questions[:3]  # Limit to 3 questions
            except json.JSONDecodeError:
                # Fallback: extract questions using simple parsing
                questions = []
                for line in result.split('\n'):
                    line = line.strip()
                    if line and ('?' in line) and (line[0].isdigit() or line[0] == '-'):
                        # Remove leading numbers or bullets
                        question = line.split('?')[0] + '?'
                        question = question.lstrip('0123456789.- ')
                        questions.append(question)
                
                return questions[:3]  # Limit to 3 questions
        
        except Exception as e:
            print(f"Error generating follow-up questions: {e}")
        
        # Fallback questions if generation fails
        return [
            "Can you explain more about how this concept applies in real-world scenarios?",
            "How does this relate to other CISSP domains?",
            "What are the most common misconceptions about this topic?"
        ]
    
    @staticmethod
    def generate_review_question(topic: str, llm: OllamaInterface) -> Dict[str, Any]:
        """
        Generate a review question for a topic.
        
        Args:
            topic: Topic to generate a question for
            llm: LLM interface for generating the question
            
        Returns:
            Dictionary with the question and answer
        """
        # First retrieve relevant context from the database to use as reference material
        from src.retrieval.retriever import Retriever
        retriever = Retriever()
        references = []
        
        # Get relevant documents for this topic
        retrieved_docs = retriever.retrieve(f"CISSP {topic} key concepts", top_k=3)
        if retrieved_docs:
            # Extract source information from metadata
            for doc in retrieved_docs:
                if doc["metadata"] and "source" in doc["metadata"]:
                    source = doc["metadata"]["source"]
                    page = doc["metadata"].get("page", "")
                    if source not in [ref.get("source") for ref in references]:
                        references.append({
                            "source": source,
                            "page": page,
                            "text": doc["text"][:150] + "..."  # First 150 chars as preview
                        })
        
        prompt = f"""
Generate a challenging multiple-choice question about the CISSP domain: {topic}

The question should test deep understanding of concepts, not just memorization.
Include 4 options (A, B, C, D) with one correct answer.
Explain why the correct answer is right and why the others are wrong.

Also include 1-3 specific references that support the correct answer. These should be actual CISSP study materials, books, or official guides with specific page numbers or sections when possible.

The response should be in this format (without showing the JSON structure to the user):
1. A clear question about {topic}
2. Four options labeled A through D
3. The correct answer letter
4. A detailed explanation of why the correct answer is right and why the others are wrong
5. References that support the correct answer (1-3 specific sources)
"""
        
        system_prompt = "You are a CISSP exam question generator creating challenging review questions."
        
        try:
            result = llm.generate(prompt, system_prompt, temperature=0.7)
            
            # Try to extract the question data using a more robust approach
            # First, clean up any JSON or markdown formatting
            cleaned_result = result.replace('```json', '').replace('```', '').strip()
            
            # Try to parse as JSON if the response appears to be in JSON format
            if cleaned_result.startswith('{') and cleaned_result.endswith('}'): 
                try:
                    question_data = json.loads(cleaned_result)
                    # Ensure the question doesn't contain JSON formatting
                    if isinstance(question_data.get('question'), str):
                        question_data['question'] = question_data['question'].replace('```json', '').replace('```', '')
                    if isinstance(question_data.get('explanation'), str):
                        question_data['explanation'] = question_data['explanation'].replace('```json', '').replace('```', '')
                    return question_data
                except json.JSONDecodeError:
                    pass  # Fall through to the parsing approach
            
            # Fallback: extract question data using structured parsing
            lines = result.split('\n')
            question = ""
            options = []
            correct_answer = ""
            explanation = ""
            
            # Simple state machine for parsing
            state = "question"
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Check for option markers to transition to options state
                if state == "question" and (line.startswith(("A)", "A.", "A:")) or 
                                          line.startswith(("Option A", "A -", "(A)"))): 
                    state = "options"
                
                if state == "question":
                    # Skip lines that look like JSON formatting or markdown
                    if not (line.startswith('{') or line.startswith('"') or line.startswith('```')):
                        question += line + " "
                
                elif state == "options":
                    # Capture options with various formats (A., A:, A), etc.)
                    option_match = False
                    for prefix in [("A", "a"), ("B", "b"), ("C", "c"), ("D", "d")]:
                        if any(line.startswith(f"{p}{s}") for p in prefix for s in [")", ".", ":", " -", ". "]):
                            options.append(line)
                            option_match = True
                            break
                    
                    # If we've collected all options, move to answer state
                    if len(options) == 4:
                        state = "answer"
                    
                    # Check for correct answer indicator
                    if not option_match and ("correct answer" in line.lower() or 
                                           "answer:" in line.lower() or 
                                           "correct:" in line.lower()):
                        state = "answer"
                        # Try to extract the answer letter
                        for letter in ["A", "B", "C", "D"]:
                            if letter in line:
                                correct_answer = letter
                                break
                
                elif state == "answer" and not correct_answer:
                    # Try to find the correct answer letter
                    if any(marker in line.lower() for marker in ["correct", "answer"]):
                        for letter in ["A", "B", "C", "D"]:
                            if letter in line:
                                correct_answer = letter
                                state = "explanation"
                                break
                
                elif state == "explanation" or (state == "answer" and correct_answer):
                    # Skip lines that look like JSON formatting
                    if not (line.startswith('}') or line.startswith('"')):
                        explanation += line + " "
            
            # Clean up the explanation to remove any JSON artifacts
            explanation = explanation.replace('"explanation":', '').replace('"', '').strip()
            
            # Ensure we have valid options
            if len(options) < 4:
                # Create default options if we couldn't parse them
                options = [
                    "A) Option A",
                    "B) Option B",
                    "C) Option C",
                    "D) Option D"
                ]
            
            # Extract references if present
            references_list = []
            if "references:" in result.lower() or "reference:" in result.lower() or "sources:" in result.lower() or "source:" in result.lower():
                ref_section = False
                ref_text = ""
                
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                        
                    # Check for reference section markers
                    if not ref_section and any(marker in line.lower() for marker in ["references:", "reference:", "sources:", "source:"]):
                        ref_section = True
                        continue
                        
                    if ref_section:
                        ref_text += line + "\n"
                
                # Process reference text into individual references
                if ref_text:
                    # Split by common reference separators
                    ref_items = []
                    if "\n" in ref_text:
                        # Split by newlines if they appear to be separate references
                        potential_refs = ref_text.split("\n")
                        for ref in potential_refs:
                            if ref and len(ref.strip()) > 10:  # Minimum length to be a reference
                                ref_items.append(ref.strip())
                    else:
                        # Single reference or comma-separated list
                        ref_items = [ref.strip() for ref in ref_text.split(",") if ref.strip()]                
                    
                    # Clean up references and add to list
                    for i, ref in enumerate(ref_items):
                        # Remove numbering if present
                        if ref and len(ref) > 3 and ref[0].isdigit() and ref[1:3] in [". ", ") ", ": "]:
                            ref = ref[3:]
                        if ref and len(ref.strip()) > 5:  # Ensure it's not empty after cleaning
                            references_list.append({
                                "id": i+1,
                                "text": ref.strip()
                            })
            
            # If no references were found in the LLM output, use the retrieved documents
            if not references_list and retrieved_docs:
                for i, doc in enumerate(retrieved_docs[:3]):  # Use up to 3 references
                    if doc["metadata"] and "source" in doc["metadata"]:
                        source = doc["metadata"]["source"]
                        page = doc["metadata"].get("page", "")
                        source_text = f"{source}"
                        if page:
                            source_text += f", page {page}"
                        references_list.append({
                            "id": i+1,
                            "text": source_text
                        })
            
            return {
                "question": question.strip(),
                "options": options,
                "correct_answer": correct_answer or "A",  # Default if parsing fails
                "explanation": explanation.strip(),
                "references": references_list
            }
        
        except Exception as e:
            print(f"Error generating review question: {e}")
        
        # Fallback question if generation fails
        return {
            "question": f"Which of the following best describes a key concept in {topic}?",
            "options": [
                "A) A placeholder option for demonstration",
                "B) A placeholder option for demonstration",
                "C) A placeholder option for demonstration",
                "D) A placeholder option for demonstration"
            ],
            "correct_answer": "A",
            "explanation": "This is a placeholder question. Please try again later."
        }


class CISSPTutor:
    """
    Main tutoring system for CISSP exam preparation.
    """
    
    def __init__(self):
        """
        Initialize the CISSP tutor.
        """
        self.retriever = Retriever()
        self.llm = OllamaInterface()
        self.prompt_builder = RAGPromptBuilder()
        self.sessions = {}  # user_id -> UserSession
        
        # Check if LLM is available
        if not self.llm.is_available():
            print("Warning: Ollama LLM is not available. Please ensure it is running.")
    
    def get_or_create_session(self, user_id: str) -> UserSession:
        """
        Get an existing session or create a new one.
        
        Args:
            user_id: User ID
            
        Returns:
            User session
        """
        if user_id not in self.sessions:
            self.sessions[user_id] = UserSession(user_id)
        
        return self.sessions[user_id]
    
    def answer_question(self, user_id: str, query: str) -> Dict[str, Any]:
        """
        Answer a user's question using RAG.
        
        Args:
            user_id: User ID
            query: User query
            
        Returns:
            Dictionary with the response and metadata
        """
        session = self.get_or_create_session(user_id)
        
        # Analyze the query
        analysis = AdaptiveLearning.analyze_query(query)
        
        # Retrieve relevant context
        results = self.retriever.retrieve(query)
        
        # Check for contradictions
        contradictions = self.retriever.detect_contradictions(results)
        
        # Format context for the LLM
        context = self.retriever.format_context(results)
        
        # Build the prompt
        system_prompt = self.prompt_builder.build_system_prompt()
        qa_prompt = self.prompt_builder.build_qa_prompt(query, context)
        
        # Generate the answer
        answer = self.llm.generate(qa_prompt, system_prompt)
        
        # Handle contradictions if any
        contradiction_explanation = ""
        if contradictions["has_contradictions"]:
            contradiction_prompt = self.prompt_builder.build_contradiction_prompt(
                query, contradictions
            )
            contradiction_explanation = self.llm.generate(
                contradiction_prompt, system_prompt
            )
        
        # Generate follow-up questions
        follow_up_questions = AdaptiveLearning.generate_follow_up_questions(
            query, answer, self.llm
        )
        
        # Prepare the response
        response = {
            "answer": answer,
            "sources": [result["metadata"] for result in results],
            "has_contradictions": contradictions["has_contradictions"],
            "contradiction_explanation": contradiction_explanation if contradictions["has_contradictions"] else "",
            "follow_up_questions": follow_up_questions,
            "topics": analysis["topics"]
        }
        
        # Update the session
        session.add_interaction(query, answer, {
            "analysis": analysis,
            "sources": [result["metadata"] for result in results],
            "has_contradictions": contradictions["has_contradictions"]
        })
        
        # Update topic strengths based on the query
        for topic in analysis["topics"]:
            # This is a simple placeholder logic
            # In a real implementation, this would be more sophisticated
            current_strength = session.topic_strengths.get(topic, 0.5)
            # Assume asking about a topic slightly increases strength
            new_strength = min(1.0, current_strength + 0.05)
            session.update_topic_strength(topic, new_strength)
        
        return response
    
    def generate_review_question(self, user_id: str, topic: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a review question for a user.
        
        Args:
            user_id: User ID
            topic: Specific topic to generate a question for (optional)
            
        Returns:
            Dictionary with the question data
        """
        session = self.get_or_create_session(user_id)
        
        # If no topic is specified, choose a weak topic
        if not topic:
            weak_topics = session.get_weak_topics()
            if weak_topics:
                topic = weak_topics[0]
            else:
                # Default to a random CISSP domain
                import random
                domains = [
                    "Security and Risk Management",
                    "Asset Security",
                    "Security Architecture and Engineering",
                    "Communication and Network Security",
                    "Identity and Access Management",
                    "Security Assessment and Testing",
                    "Security Operations",
                    "Software Development Security"
                ]
                topic = random.choice(domains)
        
        # Generate the question
        question_data = AdaptiveLearning.generate_review_question(topic, self.llm)
        
        # Add metadata
        question_data["topic"] = topic
        question_data["timestamp"] = datetime.now().isoformat()
        
        return question_data
    
    def evaluate_answer(self, user_id: str, question_id: str, user_answer: str) -> Dict[str, Any]:
        """
        Evaluate a user's answer to a review question.
        
        Args:
            user_id: User ID
            question_id: Question ID
            user_answer: User's answer
            
        Returns:
            Dictionary with evaluation results
        """
        # This is a placeholder for a more sophisticated evaluation system
        # In a real implementation, this would compare the user's answer to the correct answer
        
        # For now, just check if the answer matches the correct letter
        session = self.get_or_create_session(user_id)
        
        # In a real implementation, we would retrieve the question from storage
        # For now, we'll just return a placeholder
        
        is_correct = user_answer.upper() == "A"  # Placeholder
        
        # Update topic strength based on correctness
        # This is a simple placeholder logic
        topic = "Security and Risk Management"  # Placeholder
        current_strength = session.topic_strengths.get(topic, 0.5)
        
        if is_correct:
            # Increase strength if correct
            new_strength = min(1.0, current_strength + 0.1)
        else:
            # Decrease strength if incorrect
            new_strength = max(0.0, current_strength - 0.1)
        
        session.update_topic_strength(topic, new_strength)
        
        return {
            "is_correct": is_correct,
            "correct_answer": "A",  # Placeholder
            "explanation": "This is a placeholder explanation.",  # Placeholder
            "topic": topic,
            "new_strength": new_strength
        }
    
    def save_all_sessions(self) -> None:
        """
        Save all active sessions to files.
        """
        for user_id, session in self.sessions.items():
            session.save_to_file()


if __name__ == "__main__":
    # Test the CISSP tutor
    tutor = CISSPTutor()
    
    # Test with a sample question
    test_user_id = "test_user"
    test_query = "What is the difference between authentication and authorization in access control?"
    
    print(f"Query: {test_query}")
    response = tutor.answer_question(test_user_id, test_query)
    
    print("\nAnswer:")
    print(response["answer"])
    
    if response["has_contradictions"]:
        print("\nContradiction Explanation:")
        print(response["contradiction_explanation"])
    
    print("\nFollow-up Questions:")
    for i, question in enumerate(response["follow_up_questions"]):
        print(f"{i+1}. {question}")
    
    # Test generating a review question
    print("\nGenerating a review question...")
    question = tutor.generate_review_question(test_user_id)
    
    print(f"\nQuestion about {question['topic']}:")
    print(question["question"])
    
    print("\nOptions:")
    for option in question["options"]:
        print(option)
    
    print(f"\nCorrect Answer: {question['correct_answer']}")
    print(f"\nExplanation: {question['explanation']}")
