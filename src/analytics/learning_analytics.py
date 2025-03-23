
from datetime import datetime, timedelta
import json
from collections import defaultdict

class LearningAnalytics:
    def __init__(self):
        self.study_sessions = defaultdict(list)
        self.topic_progress = defaultdict(dict)
        self.weak_areas = defaultdict(list)
        
    def track_study_session(self, user_id: str, topic: str, duration: int, 
                          correct_answers: int, total_questions: int):
        """Track a study session."""
        self.study_sessions[user_id].append({
            'topic': topic,
            'duration': duration,
            'correct_answers': correct_answers,
            'total_questions': total_questions,
            'timestamp': datetime.now().isoformat()
        })
        
        # Update topic progress
        if topic not in self.topic_progress[user_id]:
            self.topic_progress[user_id][topic] = {
                'total_time': 0,
                'correct_answers': 0,
                'total_questions': 0
            }
            
        self.topic_progress[user_id][topic]['total_time'] += duration
        self.topic_progress[user_id][topic]['correct_answers'] += correct_answers
        self.topic_progress[user_id][topic]['total_questions'] += total_questions
        
    def analyze_weak_areas(self, user_id: str):
        """Identify topics needing more focus."""
        weak_areas = []
        for topic, progress in self.topic_progress[user_id].items():
            if progress['total_questions'] > 0:
                accuracy = progress['correct_answers'] / progress['total_questions']
                if accuracy < 0.7:  # Less than 70% correct
                    weak_areas.append({
                        'topic': topic,
                        'accuracy': accuracy,
                        'study_time': progress['total_time']
                    })
        return sorted(weak_areas, key=lambda x: x['accuracy'])
        
    def get_study_recommendations(self, user_id: str):
        """Generate personalized study recommendations."""
        weak_areas = self.analyze_weak_areas(user_id)
        recent_topics = set(session['topic'] for session 
                          in self.study_sessions[user_id][-5:])
        
        recommendations = []
        for area in weak_areas:
            if area['topic'] not in recent_topics:
                recommendations.append({
                    'topic': area['topic'],
                    'reason': f"Accuracy: {area['accuracy']*100:.1f}%",
                    'suggested_time': max(60, area['study_time'] // 2)
                })
        
        return recommendations[:3]  # Top 3 recommendations
