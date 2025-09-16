from typing import List, Optional, Dict, Any


class User:
    def __init__(self, id: int, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        return cls(
            id=data["id"],
            name=data["name"],
            email=data["email"]
        )


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


class DataStore:
    def __init__(self):
        self._users: Dict[int, User] = {}
        self._posts: Dict[int, Post] = {}
        self._next_user_id = 1
        self._next_post_id = 1
        self._initialize_sample_data()

    def _initialize_sample_data(self):
        """Initialize with sample data"""
        # Add sample users
        sample_users = [
            {"name": "John Doe", "email": "john@example.com"},
            {"name": "Jane Smith", "email": "jane@example.com"}
        ]
        for user_data in sample_users:
            self.create_user(user_data["name"], user_data["email"])

        # Add sample posts
        sample_posts = [
            {"title": "First Post",
                "content": "This is the content of the first post", "user_id": 1},
            {"title": "Second Post",
                "content": "This is the content of the second post", "user_id": 2},
            {"title": "Third Post",
                "content": "This is the content of the third post", "user_id": 1}
        ]
        for post_data in sample_posts:
            self.create_post(
                post_data["title"], post_data["content"], post_data["user_id"])

    # User methods
    def get_all_users(self) -> List[User]:
        """Get all users"""
        return list(self._users.values())

    def get_user(self, user_id: int) -> Optional[User]:
        """Get a user by ID"""
        return self._users.get(user_id)

    def create_user(self, name: str, email: str) -> User:
        """Create a new user"""
        user_id = self._next_user_id
        self._next_user_id += 1

        user = User(id=user_id, name=name, email=email)
        self._users[user_id] = user
        return user

    def update_user(self, user_id: int, name: Optional[str] = None, email: Optional[str] = None) -> Optional[User]:
        """Update an existing user"""
        user = self._users.get(user_id)
        if not user:
            return None

        if name is not None:
            user.name = name
        if email is not None:
            user.email = email

        return user

    def delete_user(self, user_id: int) -> bool:
        """Delete a user"""
        if user_id in self._users:
            del self._users[user_id]
            # Also delete all posts by this user
            posts_to_delete = [
                post_id for post_id, post in self._posts.items() if post.user_id == user_id]
            for post_id in posts_to_delete:
                del self._posts[post_id]
            return True
        return False

    def user_exists(self, user_id: int) -> bool:
        """Check if a user exists"""
        return user_id in self._users

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email"""
        for user in self._users.values():
            if user.email == email:
                return user
        return None

    # Post methods
    def get_all_posts(self) -> List[Post]:
        """Get all posts"""
        return list(self._posts.values())

    def get_post(self, post_id: int) -> Optional[Post]:
        """Get a post by ID"""
        return self._posts.get(post_id)

    def create_post(self, title: str, content: str, user_id: int) -> Optional[Post]:
        """Create a new post"""
        if not self.user_exists(user_id):
            return None

        post_id = self._next_post_id
        self._next_post_id += 1

        post = Post(id=post_id, title=title, content=content, user_id=user_id)
        self._posts[post_id] = post
        return post

    def update_post(self, post_id: int, title: Optional[str] = None, content: Optional[str] = None, user_id: Optional[int] = None) -> Optional[Post]:
        """Update an existing post"""
        post = self._posts.get(post_id)
        if not post:
            return None

        if user_id is not None and not self.user_exists(user_id):
            return None

        if title is not None:
            post.title = title
        if content is not None:
            post.content = content
        if user_id is not None:
            post.user_id = user_id

        return post

    def delete_post(self, post_id: int) -> bool:
        """Delete a post"""
        if post_id in self._posts:
            del self._posts[post_id]
            return True
        return False

    def get_posts_by_user(self, user_id: int) -> List[Post]:
        """Get all posts by a specific user"""
        if not self.user_exists(user_id):
            return []
        return [post for post in self._posts.values() if post.user_id == user_id]


# Global data store instance
data_store = DataStore()
