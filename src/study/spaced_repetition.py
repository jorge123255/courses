
from datetime import datetime, timedelta
import json
from typing import Dict, List

class SpacedRepetitionSystem:
    def __init__(self):
        self.intervals = [1, 3, 7, 14, 30, 90]  # Days between reviews
        
    def calculate_next_review(self, current_level: int) -> datetime:
        if current_level >= len(self.intervals):
            current_level = len(self.intervals) - 1
        days = self.intervals[current_level]
        return datetime.now() + timedelta(days=days)
        
    def process_response(self, card_id: str, user_data: Dict) -> Dict:
        if card_id not in user_data:
            user_data[card_id] = {"level": 0, "next_review": datetime.now()}
        
        card_data = user_data[card_id]
        if card_data["level"] < len(self.intervals):
            card_data["level"] += 1
            
        card_data["next_review"] = self.calculate_next_review(card_data["level"])
        return user_data
