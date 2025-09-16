from typing import Dict, Any


class Post:
    def __init__(self, id: int, title: str, content: str, user_id: int):
        self.id = id
        self.title = title
        self.content = content
        self.user_id = user_id

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "user_id": self.user_id
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Post':
        return cls(
            id=data["id"],
            title=data["title"],
            content=data["content"],
            user_id=data["user_id"]
        )
