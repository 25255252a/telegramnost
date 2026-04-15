from datetime import datetime

class Message:
    def __init__(self, user_id, content, message_id=None, timestamp=None):
        self.id = message_id
        self.user_id = user_id
        self.content = content
        self.timestamp = timestamp or datetime.now()
