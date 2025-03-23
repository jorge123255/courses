
class StudyGroup:
    def __init__(self):
        self.groups = {}
        
    def create_group(self, group_name, creator_id):
        """Create a new study group."""
        group_id = str(uuid.uuid4())
        self.groups[group_id] = {
            'name': group_name,
            'creator': creator_id,
            'members': [creator_id],
            'discussions': []
        }
        return group_id
        
    def add_discussion(self, group_id, user_id, topic, content):
        """Add a discussion topic to the group."""
        if group_id in self.groups:
            self.groups[group_id]['discussions'].append({
                'topic': topic,
                'content': content,
                'user_id': user_id,
                'timestamp': datetime.now(),
                'responses': []
            })
