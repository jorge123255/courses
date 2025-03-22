
from dataclasses import dataclass
from typing import Optional, List
import json
import os
from datetime import datetime

@dataclass
class User:
    id: str
    username: str
    email: Optional[str]
    roles: List[str]
    created_at: str
    
class AuthManager:
    def __init__(self):
        self.users_file = "data/users.json"
        self._load_users()
    
    def _load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        else:
            os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
            self.users = {}
            self._save_users()
    
    def _save_users(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def authenticate_user(self, user_id: str, username: str) -> bool:
        if user_id not in self.users:
            # New user
            self.users[user_id] = {
                "username": username,
                "email": None,
                "roles": ["user"],
                "created_at": datetime.now().isoformat()
            }
            self._save_users()
        return True
    
    def get_user(self, user_id: str) -> Optional[User]:
        if user_id in self.users:
            data = self.users[user_id]
            return User(
                id=user_id,
                username=data["username"],
                email=data["email"],
                roles=data["roles"],
                created_at=data["created_at"]
            )
        return None

    def update_user_email(self, user_id: str, email: str) -> bool:
        if user_id in self.users:
            self.users[user_id]["email"] = email
            self._save_users()
            return True
        return False

    def is_admin(self, user_id: str) -> bool:
        return user_id in self.users and "admin" in self.users[user_id]["roles"]
