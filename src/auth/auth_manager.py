
"""Authentication manager for CISSP Tutor."""
import os
import json
from datetime import datetime
from typing import Optional
from dataclasses import dataclass
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@dataclass
class User(UserMixin):
    id: str
    username: str
    email: str
    roles: list
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
    
    def register_user(self, username: str, email: str, password: str) -> bool:
        user_id = str(hash(f"{username}{email}{datetime.now().isoformat()}"))
        
        if user_id not in self.users:
            self.users[user_id] = {
                "username": username,
                "email": email,
                "password": generate_password_hash(password),
                "roles": ["user"],
                "created_at": datetime.now().isoformat()
            }
            self._save_users()
            return True
        return False

    def authenticate_user(self, email: str, password: str) -> Optional[str]:
        for user_id, user_data in self.users.items():
            if user_data["email"] == email and check_password_hash(user_data["password"], password):
                return user_id
        return None

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

    def is_admin(self, user_id: str) -> bool:
        return user_id in self.users and "admin" in self.users[user_id]["roles"]
