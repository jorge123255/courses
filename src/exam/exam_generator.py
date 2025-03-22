"""
Exam generator module for creating practice exams.
"""
import os
import json
import random
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import config
from src.retrieval.llm_interface import OllamaInterface, RAGPromptBuilder
from src.tutoring.tutor import AdaptiveLearning


class ExamQuestion:
    """
    Represents a single exam question.
    """
    
    def __init__(self, question_id: str, question_text: str, options: List[str], 
                 correct_answer: str, explanation: str, topic: str, difficulty: float = 0.5):
        """
        Initialize an exam question.
        
        Args:
            question_id: Unique identifier for the question
            question_text: Text of the question
            options: List of answer options
            correct_answer: Correct answer option
            explanation: Explanation of the correct answer
            topic: Topic/domain the question belongs to
            difficulty: Difficulty level (0.0 to 1.0)
        """
        self.question_id = question_id
        self.question_text = question_text
        self.options = options
        self.correct_answer = correct_answer
        self.explanation = explanation
        self.topic = topic
        self.difficulty = difficulty
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the question to a dictionary.
        
        Returns:
            Dictionary representation of the question
        """
        return {
            "question_id": self.question_id,
            "question_text": self.question_text,
            "options": self.options,
            "correct_answer": self.correct_answer,
            "explanation": self.explanation,
            "topic": self.topic,
            "difficulty": self.difficulty,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ExamQuestion':
        """
        Create a question from a dictionary.
        
        Args:
            data: Dictionary representation of the question
            
        Returns:
            ExamQuestion object
        """
        return cls(
            question_id=data["question_id"],
            question_text=data["question_text"],
            options=data["options"],
            correct_answer=data["correct_answer"],
            explanation=data["explanation"],
            topic=data["topic"],
            difficulty=data.get("difficulty", 0.5)
        )


class Exam:
    """
    Represents a complete exam with multiple questions.
    """
    
    def __init__(self, exam_id: str, title: str, description: str = "", 
                 time_limit_minutes: int = 120, passing_score: float = 0.7):
        """
        Initialize an exam.
        
        Args:
            exam_id: Unique identifier for the exam
            title: Title of the exam
            description: Description of the exam
            time_limit_minutes: Time limit in minutes
            passing_score: Passing score (0.0 to 1.0)
        """
        self.exam_id = exam_id
        self.title = title
        self.description = description
        self.time_limit_minutes = time_limit_minutes
        self.passing_score = passing_score
        self.questions = []
        self.created_at = datetime.now().isoformat()
    
    def add_question(self, question: ExamQuestion) -> None:
        """
        Add a question to the exam.
        
        Args:
            question: Question to add
        """
        self.questions.append(question)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the exam to a dictionary.
        
        Returns:
            Dictionary representation of the exam
        """
        return {
            "exam_id": self.exam_id,
            "title": self.title,
            "description": self.description,
            "time_limit_minutes": self.time_limit_minutes,
            "passing_score": self.passing_score,
            "questions": [q.to_dict() for q in self.questions],
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Exam':
        """
        Create an exam from a dictionary.
        
        Args:
            data: Dictionary representation of the exam
            
        Returns:
            Exam object
        """
        exam = cls(
            exam_id=data["exam_id"],
            title=data["title"],
            description=data["description"],
            time_limit_minutes=data["time_limit_minutes"],
            passing_score=data["passing_score"]
        )
        
        for q_data in data["questions"]:
            question = ExamQuestion.from_dict(q_data)
            exam.add_question(question)
        
        return exam
    
    def save_to_file(self, directory: str = None) -> str:
        """
        Save the exam to a file.
        
        Args:
            directory: Directory to save the file in
            
        Returns:
            Path to the saved file
        """
        directory = directory or os.path.join(config.DATA_DIR, "exams")
        os.makedirs(directory, exist_ok=True)
        
        filename = f"{self.exam_id}.json"
        filepath = os.path.join(directory, filename)
        
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
        
        return filepath
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'Exam':
        """
        Load an exam from a file.
        
        Args:
            filepath: Path to the exam file
            
        Returns:
            Loaded Exam object
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        return cls.from_dict(data)


class ExamAttempt:
    """
    Represents a user's attempt at an exam.
    """
    
    def __init__(self, attempt_id: str, user_id: str, exam_id: str):
        """
        Initialize an exam attempt.
        
        Args:
            attempt_id: Unique identifier for the attempt
            user_id: User ID
            exam_id: Exam ID
        """
        self.attempt_id = attempt_id
        self.user_id = user_id
        self.exam_id = exam_id
        self.started_at = datetime.now().isoformat()
        self.completed_at = None
        self.answers = {}  # question_id -> answer
        self.score = 0.0
        self.feedback = {}  # question_id -> feedback
    
    def answer_question(self, question_id: str, answer: str) -> None:
        """
        Record an answer to a question.
        
        Args:
            question_id: Question ID
            answer: User's answer
        """
        self.answers[question_id] = answer
    
    def complete(self, exam: Exam) -> float:
        """
        Complete the attempt and calculate the score.
        
        Args:
            exam: The exam that was attempted
            
        Returns:
            Score (0.0 to 1.0)
        """
        self.completed_at = datetime.now().isoformat()
        
        correct_count = 0
        for question in exam.questions:
            user_answer = self.answers.get(question.question_id)
            if user_answer == question.correct_answer:
                correct_count += 1
                self.feedback[question.question_id] = {
                    "is_correct": True,
                    "explanation": question.explanation
                }
            else:
                self.feedback[question.question_id] = {
                    "is_correct": False,
                    "correct_answer": question.correct_answer,
                    "explanation": question.explanation
                }
        
        self.score = correct_count / len(exam.questions) if exam.questions else 0.0
        return self.score
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the attempt to a dictionary.
        
        Returns:
            Dictionary representation of the attempt
        """
        return {
            "attempt_id": self.attempt_id,
            "user_id": self.user_id,
            "exam_id": self.exam_id,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "answers": self.answers,
            "score": self.score,
            "feedback": self.feedback
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ExamAttempt':
        """
        Create an attempt from a dictionary.
        
        Args:
            data: Dictionary representation of the attempt
            
        Returns:
            ExamAttempt object
        """
        attempt = cls(
            attempt_id=data["attempt_id"],
            user_id=data["user_id"],
            exam_id=data["exam_id"]
        )
        
        attempt.started_at = data["started_at"]
        attempt.completed_at = data["completed_at"]
        attempt.answers = data["answers"]
        attempt.score = data["score"]
        attempt.feedback = data["feedback"]
        
        return attempt
    
    def save_to_file(self, directory: str = None) -> str:
        """
        Save the attempt to a file.
        
        Args:
            directory: Directory to save the file in
            
        Returns:
            Path to the saved file
        """
        directory = directory or os.path.join(config.DATA_DIR, "attempts")
        os.makedirs(directory, exist_ok=True)
        
        filename = f"{self.attempt_id}.json"
        filepath = os.path.join(directory, filename)
        
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
        
        return filepath
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'ExamAttempt':
        """
        Load an attempt from a file.
        
        Args:
            filepath: Path to the attempt file
            
        Returns:
            Loaded ExamAttempt object
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        return cls.from_dict(data)


class ExamGenerator:
    """
    Generates practice exams for CISSP preparation.
    """
    
    def __init__(self):
        """
        Initialize the exam generator.
        """
        self.llm = OllamaInterface()
        self.prompt_builder = RAGPromptBuilder()
        
        # CISSP domains
        self.domains = [
            "Security and Risk Management",
            "Asset Security",
            "Security Architecture and Engineering",
            "Communication and Network Security",
            "Identity and Access Management",
            "Security Assessment and Testing",
            "Security Operations",
            "Software Development Security"
        ]
        
        # Check if LLM is available
        if not self.llm.is_available():
            print("Warning: Ollama LLM is not available. Please ensure it is running.")
    
    def generate_question(self, topic: str, difficulty: float = 0.5) -> ExamQuestion:
        """
        Generate a single exam question.
        
        Args:
            topic: Topic/domain for the question
            difficulty: Difficulty level (0.0 to 1.0)
            
        Returns:
            Generated ExamQuestion
        """
        # Adjust the prompt based on difficulty
        difficulty_desc = "basic"
        if difficulty > 0.7:
            difficulty_desc = "advanced"
        elif difficulty > 0.3:
            difficulty_desc = "intermediate"
        
        prompt = f"""
Generate a {difficulty_desc} multiple-choice question for the CISSP exam on the topic of {topic}.

The question should:
1. Be clear and unambiguous
2. Have 4 options (A, B, C, D)
3. Have exactly one correct answer
4. Include a detailed explanation of why the correct answer is right and why the others are wrong

Format your response as a JSON object with these fields:
- question_text: the question text
- options: array of 4 option strings (starting with A, B, C, D)
- correct_answer: the letter of the correct option (A, B, C, or D)
- explanation: detailed explanation of the correct answer and why others are incorrect
"""
        
        system_prompt = "You are a CISSP exam question generator creating high-quality practice questions."
        
        try:
            result = self.llm.generate(prompt, system_prompt, temperature=0.7)
            
            # Try to parse as JSON
            try:
                data = json.loads(result)
                
                # Create the question
                question_id = str(uuid.uuid4())
                return ExamQuestion(
                    question_id=question_id,
                    question_text=data["question_text"],
                    options=data["options"],
                    correct_answer=data["correct_answer"],
                    explanation=data["explanation"],
                    topic=topic,
                    difficulty=difficulty
                )
            except json.JSONDecodeError:
                # Fallback: extract question data using simple parsing
                # This is a simplified version of the parsing in AdaptiveLearning.generate_review_question
                lines = result.split('\n')
                question_text = ""
                options = []
                correct_answer = ""
                explanation = ""
                
                # Simple state machine for parsing
                state = "question"
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    
                    if state == "question" and line.startswith(("A)", "A.", "A:")):
                        state = "options"
                    
                    if state == "question":
                        question_text += line + " "
                    elif state == "options":
                        if line.startswith(("A)", "A.", "A:")):
                            options.append(line)
                        elif line.startswith(("B)", "B.", "B:")):
                            options.append(line)
                        elif line.startswith(("C)", "C.", "C:")):
                            options.append(line)
                        elif line.startswith(("D)", "D.", "D:")):
                            options.append(line)
                            state = "answer"
                        elif line.lower().startswith("correct answer"):
                            state = "answer"
                            correct_answer = line.split(":")[-1].strip()
                    elif state == "answer" and not correct_answer:
                        if "correct" in line.lower() or "answer" in line.lower():
                            correct_answer = line.split(":")[-1].strip()
                            state = "explanation"
                    elif state == "explanation" or (state == "answer" and correct_answer):
                        explanation += line + " "
                
                # Create the question
                question_id = str(uuid.uuid4())
                return ExamQuestion(
                    question_id=question_id,
                    question_text=question_text.strip(),
                    options=options or ["A) Option A", "B) Option B", "C) Option C", "D) Option D"],
                    correct_answer=correct_answer or "A",
                    explanation=explanation.strip() or "Explanation not available",
                    topic=topic,
                    difficulty=difficulty
                )
        
        except Exception as e:
            print(f"Error generating question: {e}")
            
            # Fallback question
            question_id = str(uuid.uuid4())
            return ExamQuestion(
                question_id=question_id,
                question_text=f"What is a key concept in {topic}?",
                options=[
                    "A) A placeholder option for demonstration",
                    "B) A placeholder option for demonstration",
                    "C) A placeholder option for demonstration",
                    "D) A placeholder option for demonstration"
                ],
                correct_answer="A",
                explanation="This is a placeholder question. Please try again later.",
                topic=topic,
                difficulty=difficulty
            )
    
    def generate_exam(self, title: str, description: str = "", 
                      question_count: int = 10, time_limit_minutes: int = 120,
                      domain_weights: Optional[Dict[str, float]] = None) -> Exam:
        """
        Generate a complete exam.
        
        Args:
            title: Title of the exam
            description: Description of the exam
            question_count: Number of questions to generate
            time_limit_minutes: Time limit in minutes
            domain_weights: Weights for each domain (domain -> weight)
            
        Returns:
            Generated Exam
        """
        # Create the exam
        exam_id = str(uuid.uuid4())
        exam = Exam(
            exam_id=exam_id,
            title=title,
            description=description,
            time_limit_minutes=time_limit_minutes
        )
        
        # Determine the number of questions per domain
        if domain_weights is None:
            # Equal distribution by default
            domain_weights = {domain: 1.0 for domain in self.domains}
        
        # Normalize weights
        total_weight = sum(domain_weights.values())
        normalized_weights = {d: w / total_weight for d, w in domain_weights.items()}
        
        # Calculate questions per domain
        questions_per_domain = {}
        remaining = question_count
        
        for domain, weight in normalized_weights.items():
            count = int(question_count * weight)
            questions_per_domain[domain] = count
            remaining -= count
        
        # Distribute remaining questions
        for domain in sorted(normalized_weights, key=normalized_weights.get, reverse=True):
            if remaining <= 0:
                break
            questions_per_domain[domain] += 1
            remaining -= 1
        
        # Generate questions for each domain
        for domain, count in questions_per_domain.items():
            for _ in range(count):
                # Vary difficulty
                difficulty = random.uniform(0.3, 0.9)
                question = self.generate_question(domain, difficulty)
                exam.add_question(question)
        
        return exam
    
    def generate_domain_specific_exam(self, domain: str, question_count: int = 10) -> Exam:
        """
        Generate an exam focused on a specific domain.
        
        Args:
            domain: CISSP domain to focus on
            question_count: Number of questions to generate
            
        Returns:
            Generated domain-specific Exam
        """
        title = f"CISSP {domain} Practice Exam"
        description = f"A practice exam focused on the {domain} domain of the CISSP certification."
        
        # Create domain weights (all weight on the specified domain)
        domain_weights = {d: 0.1 for d in self.domains}
        domain_weights[domain] = 10.0  # Much higher weight for the specified domain
        
        return self.generate_exam(
            title=title,
            description=description,
            question_count=question_count,
            domain_weights=domain_weights
        )
    
    def generate_adaptive_exam(self, user_id: str, question_count: int = 10) -> Exam:
        """
        Generate an adaptive exam based on user's weak areas.
        
        Args:
            user_id: User ID
            question_count: Number of questions to generate
            
        Returns:
            Generated adaptive Exam
        """
        # This is a placeholder for a more sophisticated adaptive exam generator
        # In a real implementation, this would analyze the user's performance history
        
        title = f"CISSP Adaptive Practice Exam"
        description = "A practice exam tailored to your weak areas in the CISSP domains."
        
        # For now, just generate a random exam
        return self.generate_exam(
            title=title,
            description=description,
            question_count=question_count
        )


if __name__ == "__main__":
    # Test the exam generator
    generator = ExamGenerator()
    
    # Test generating a single question
    print("Generating a sample question...")
    question = generator.generate_question("Security and Risk Management")
    
    print(f"\nQuestion: {question.question_text}")
    print("\nOptions:")
    for option in question.options:
        print(option)
    
    print(f"\nCorrect Answer: {question.correct_answer}")
    print(f"\nExplanation: {question.explanation}")
    
    # Test generating a complete exam
    print("\nGenerating a sample exam...")
    exam = generator.generate_exam(
        title="CISSP Practice Exam",
        description="A practice exam for CISSP certification preparation",
        question_count=3  # Small number for testing
    )
    
    print(f"\nExam: {exam.title}")
    print(f"Description: {exam.description}")
    print(f"Questions: {len(exam.questions)}")
    
    # Save the exam
    filepath = exam.save_to_file()
    print(f"\nExam saved to: {filepath}")
    
    # Test loading the exam
    loaded_exam = Exam.load_from_file(filepath)
    print(f"\nLoaded exam: {loaded_exam.title}")
    print(f"Loaded questions: {len(loaded_exam.questions)}")
