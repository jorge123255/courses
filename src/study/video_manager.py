
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
