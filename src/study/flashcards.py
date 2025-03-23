
from typing import List, Dict
import json
import random

class FlashcardSystem:
    def __init__(self):
        self.cards = {}
        
    def add_card(self, topic: str, front: str, back: str) -> str:
        card_id = str(len(self.cards))
        self.cards[card_id] = {
            "topic": topic,
            "front": front,
            "back": back
        }
        return card_id
        
    def get_cards_by_topic(self, topic: str) -> List[Dict]:
        return [card for card in self.cards.values() if card["topic"] == topic]
        
    def get_random_card(self, topic: str = None) -> Dict:
        available_cards = self.get_cards_by_topic(topic) if topic else list(self.cards.values())
        return random.choice(available_cards) if available_cards else None
