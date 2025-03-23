
from datetime import datetime
from typing import Dict, List
import json

class ProgressTracker:
    def __init__(self):
        self.study_sessions = []
        self.quiz_results = []
        
    def log_study_session(self, user_id: str, topic: str, duration: int):
        self.study_sessions.append({
            "user_id": user_id,
            "topic": topic,
            "duration": duration,
            "timestamp": datetime.now().isoformat()
        })
        
    def log_quiz_result(self, user_id: str, topic: str, score: float, questions: int):
        self.quiz_results.append({
            "user_id": user_id,
            "topic": topic,
            "score": score,
            "questions": questions,
            "timestamp": datetime.now().isoformat()
        })
        
    def get_user_progress(self, user_id: str) -> Dict:
        return {
            "total_study_time": sum(s["duration"] for s in self.study_sessions if s["user_id"] == user_id),
            "average_score": sum(q["score"] for q in self.quiz_results if q["user_id"] == user_id) / 
                           len([q for q in self.quiz_results if q["user_id"] == user_id]) if self.quiz_results else 0,
            "topics_studied": list(set(s["topic"] for s in self.study_sessions if s["user_id"] == user_id))
        }
