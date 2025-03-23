
from typing import Dict, List, Optional
import json
import os

class VideoManager:
    def __init__(self):
        self.videos = {}
        self._load_videos()
    
    def _load_videos(self):
        """Load video mappings from storage if available"""
        if os.path.exists('data/video_content.json'):
            with open('data/video_content.json', 'r') as f:
                self.videos = json.load(f)
    
    def save_videos(self):
        """Save video mappings to storage"""
        os.makedirs('data', exist_ok=True)
        with open('data/video_content.json', 'w') as f:
            json.dump(self.videos, f)
    
    def add_video(self, topic: str, title: str, url: str, description: str = ""):
        """Add a video for a specific topic"""
        if topic not in self.videos:
            self.videos[topic] = []
        
        self.videos[topic].append({
            "title": title,
            "url": url,
            "description": description
        })
        self.save_videos()
    
    def get_videos(self, topic: str) -> List[Dict]:
        """Get all videos for a specific topic"""
        return self.videos.get(topic, [])
    
    def get_all_topics(self) -> List[str]:
        """Get all topics with videos"""
        return list(self.videos.keys())
from datetime import datetime
import json
import os

class VideoManager:
    def __init__(self):
        self.videos = {}
        self.watch_history = {}
        
    def add_video(self, topic: str, title: str, url: str, duration: int, description: str):
        """Add a new video resource."""
        video_id = str(hash(f"{topic}_{title}_{url}"))
        self.videos[video_id] = {
            'topic': topic,
            'title': title,
            'url': url,
            'duration': duration,
            'description': description,
            'added_at': datetime.now().isoformat()
        }
        return video_id
        
    def get_videos_by_topic(self, topic: str):
        """Get all videos for a specific topic."""
        return {vid_id: vid for vid_id, vid in self.videos.items() 
               if vid['topic'].lower() == topic.lower()}
        
    def track_watch_progress(self, user_id: str, video_id: str, progress: float):
        """Track user's video watching progress."""
        if user_id not in self.watch_history:
            self.watch_history[user_id] = {}
            
        self.watch_history[user_id][video_id] = {
            'progress': progress,
            'last_watched': datetime.now().isoformat()
        }
