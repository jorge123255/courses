
from datetime import datetime, timedelta
import json
import os

class StudyPlanner:
    def __init__(self):
        self.study_goals = {}
        self.progress = {}
        
    def set_study_goal(self, user_id, domain, target_date):
        """Set a study goal for a specific domain."""
        if user_id not in self.study_goals:
            self.study_goals[user_id] = {}
        
        self.study_goals[user_id][domain] = {
            'target_date': target_date,
            'created_at': datetime.now(),
            'completed': False
        }
        
    def track_progress(self, user_id, domain, minutes_studied):
        """Track study progress for a domain."""
        if user_id not in self.progress:
            self.progress[user_id] = {}
        
        if domain not in self.progress[user_id]:
            self.progress[user_id][domain] = 0
            
        self.progress[user_id][domain] += minutes_studied
