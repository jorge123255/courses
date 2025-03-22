#!/usr/bin/env python
"""
Command-line interface for the CISSP Tutor & Exam Platform.
"""
import os
import sys
import argparse
import uuid
import json
from datetime import datetime

# Add the project root to the path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

import config
from src.ingestion.ingest import ingest_documents, ingest_pdfs
from src.tutoring.tutor import CISSPTutor
from src.exam.exam_generator import ExamGenerator, Exam, ExamAttempt


def setup_argparse():
    """Set up argument parsing for the CLI."""
    parser = argparse.ArgumentParser(description="CISSP Tutor & Exam Platform CLI")
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Ingest command
    ingest_parser = subparsers.add_parser("ingest", help="Ingest document files (PDF and EPUB)")
    ingest_parser.add_argument("--doc_dir", type=str, help="Directory containing document files")
    ingest_parser.add_argument("--pdf_dir", type=str, help="Directory containing PDF files (legacy, use --doc_dir instead)")
    ingest_parser.add_argument("--file_types", type=str, nargs="+", default=["pdf", "epub"], 
                              choices=["pdf", "epub"], help="File types to process")
    ingest_parser.add_argument("--force", action="store_true", help="Force reindexing of all documents")
    
    # Ask command
    ask_parser = subparsers.add_parser("ask", help="Ask a question")
    ask_parser.add_argument("question", type=str, help="Question to ask")
    ask_parser.add_argument("--user_id", type=str, default=None, help="User ID")
    
    # Generate exam command
    exam_parser = subparsers.add_parser("exam", help="Generate an exam")
    exam_parser.add_argument("--title", type=str, default="CISSP Practice Exam", help="Exam title")
    exam_parser.add_argument("--count", type=int, default=10, help="Number of questions")
    exam_parser.add_argument("--domain", type=str, default=None, help="Specific domain to focus on")
    exam_parser.add_argument("--output", type=str, default=None, help="Output file for the exam")
    
    # Take exam command
    take_parser = subparsers.add_parser("take", help="Take an exam")
    take_parser.add_argument("exam_file", type=str, help="Path to the exam file")
    take_parser.add_argument("--user_id", type=str, default=None, help="User ID")
    
    return parser


def handle_ingest(args):
    """Handle the ingest command."""
    # Support both --doc_dir (new) and --pdf_dir (legacy) for backward compatibility
    doc_dir = args.doc_dir or args.pdf_dir
    force_reindex = args.force
    file_types = args.file_types
    
    # Format file types for display
    file_types_str = ", ".join(file_types).upper()
    
    print(f"Ingesting {file_types_str} files from {doc_dir or config.PDF_DIR}")
    
    # Use the new ingest_documents function
    ingest_documents(doc_dir, force_reindex, file_types)
    print("Ingestion complete")


def handle_ask(args):
    """Handle the ask command."""
    question = args.question
    user_id = args.user_id or str(uuid.uuid4())
    
    print(f"Question: {question}")
    print("Thinking...")
    
    tutor = CISSPTutor()
    response = tutor.answer_question(user_id, question)
    
    print("\nAnswer:")
    print(response["answer"])
    
    if response["has_contradictions"]:
        print("\nContradictions detected:")
        print(response["contradiction_explanation"])
    
    if response["follow_up_questions"]:
        print("\nFollow-up questions:")
        for i, q in enumerate(response["follow_up_questions"]):
            print(f"{i+1}. {q}")


def handle_exam_generation(args):
    """Handle the exam generation command."""
    title = args.title
    count = args.count
    domain = args.domain
    output_file = args.output
    
    print(f"Generating exam: {title}")
    print(f"Questions: {count}")
    if domain:
        print(f"Domain: {domain}")
    
    generator = ExamGenerator()
    
    if domain:
        exam = generator.generate_domain_specific_exam(domain, count)
    else:
        exam = generator.generate_exam(title, question_count=count)
    
    if output_file:
        filepath = output_file
        with open(filepath, 'w') as f:
            json.dump(exam.to_dict(), f, indent=2)
    else:
        filepath = exam.save_to_file()
    
    print(f"Exam saved to: {filepath}")
    return filepath


def handle_take_exam(args):
    """Handle the take exam command."""
    exam_file = args.exam_file
    user_id = args.user_id or str(uuid.uuid4())
    
    # Load the exam
    exam = Exam.load_from_file(exam_file)
    
    print(f"Exam: {exam.title}")
    print(f"Description: {exam.description}")
    print(f"Questions: {len(exam.questions)}")
    print(f"Time limit: {exam.time_limit_minutes} minutes")
    print("\nStarting exam...\n")
    
    # Create a new attempt
    attempt_id = str(uuid.uuid4())
    attempt = ExamAttempt(attempt_id, user_id, exam.exam_id)
    
    # Take the exam
    for i, question in enumerate(exam.questions):
        print(f"\nQuestion {i+1} of {len(exam.questions)}")
        print(question.question_text)
        print("\nOptions:")
        for option in question.options:
            print(option)
        
        # Get the answer
        while True:
            answer = input("\nYour answer (A/B/C/D): ").strip().upper()
            if answer in ["A", "B", "C", "D"]:
                break
            print("Invalid answer. Please enter A, B, C, or D.")
        
        # Record the answer
        attempt.answer_question(question.question_id, answer)
    
    # Complete the attempt
    score = attempt.complete(exam)
    
    print("\nExam complete!")
    print(f"Score: {score * 100:.1f}%")
    print(f"Passing score: {exam.passing_score * 100:.1f}%")
    
    if score >= exam.passing_score:
        print("Congratulations! You passed the exam.")
    else:
        print("Sorry, you did not pass the exam.")
    
    # Show feedback
    print("\nFeedback:")
    for i, question in enumerate(exam.questions):
        feedback = attempt.feedback.get(question.question_id, {})
        user_answer = attempt.answers.get(question.question_id, "")
        
        print(f"\nQuestion {i+1}: {question.question_text}")
        print(f"Your answer: {user_answer}")
        print(f"Correct answer: {question.correct_answer}")
        
        if feedback.get("is_correct", False):
            print("Result: Correct")
        else:
            print("Result: Incorrect")
        
        print(f"Explanation: {question.explanation}")
    
    # Save the attempt
    filepath = attempt.save_to_file()
    print(f"\nAttempt saved to: {filepath}")


def main():
    """Main function for the CLI."""
    parser = setup_argparse()
    args = parser.parse_args()
    
    if args.command == "ingest":
        handle_ingest(args)
    elif args.command == "ask":
        handle_ask(args)
    elif args.command == "exam":
        handle_exam_generation(args)
    elif args.command == "take":
        handle_take_exam(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
