
from datetime import datetime
import json

class NoteManager:
    def __init__(self):
        self.notes = {}
        
    def add_note(self, user_id: str, topic: str, content: str, tags: list = None):
        """Add a new study note."""
        note_id = str(hash(f"{user_id}_{topic}_{datetime.now()}"))
        self.notes[note_id] = {
            'user_id': user_id,
            'topic': topic,
            'content': content,
            'tags': tags or [],
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        return note_id
        
    def get_notes_by_topic(self, user_id: str, topic: str):
        """Get all notes for a specific topic."""
        return {note_id: note for note_id, note in self.notes.items() 
               if note['user_id'] == user_id and note['topic'].lower() == topic.lower()}
        
    def search_notes(self, user_id: str, query: str):
        """Search through user's notes."""
        return {note_id: note for note_id, note in self.notes.items()
                if note['user_id'] == user_id and 
                (query.lower() in note['content'].lower() or 
                 query.lower() in note['topic'].lower() or
                 any(query.lower() in tag.lower() for tag in note['tags']))}
