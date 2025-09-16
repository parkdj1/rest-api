# REST API Project

A simple Flask-based RESTful API for managing users and posts with comprehensive testing and in-memory data storage.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

## Features

- **RESTful API Design**: Clean, REST-compliant endpoints for users and posts
- **Data Validation**: Comprehensive input validation and error handling
- **In-Memory Storage**: Simple, fast data storage using Python dictionaries
- **Comprehensive Testing**: 59 unit and integration tests with 100% endpoint coverage
- **Blueprint Architecture**: Modular code organization using Flask Blueprints
- **CORS Support**: Cross-origin resource sharing enabled
- **Type Hints**: Full type annotations for better code maintainability

## Prerequisites

- Python 3.9 or higher
- pip (Python package installer)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd rest-api
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the development server**
   ```bash
   python app.py
   ```

2. **Access the API**
   - Base URL: `http://localhost:5000`
   - API endpoints: `http://localhost:5000/api/`

3. **Test the API**
   ```bash
   curl http://localhost:5000/
   # Expected response: {"message": "Welcome to the REST API"}
   ```

## API Documentation

### Base URL
```
http://localhost:5000
```

### Authentication
No authentication is required for this API.

### Response Format
All responses are in JSON format.

### Error Responses
The API returns appropriate HTTP status codes and error messages:

- `400 Bad Request` - Invalid request data
- `404 Not Found` - Resource not found
- `409 Conflict` - Duplicate data (e.g., email already exists)
- `415 Unsupported Media Type` - Missing or invalid content-type

### Users Endpoints

#### Get All Users
```http
GET /api/users/
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com"
  },
  {
    "id": 2,
    "name": "Jane Smith",
    "email": "jane@example.com"
  }
]
```

#### Get User by ID
```http
GET /api/users/{id}
```

**Parameters:**
- `id` (integer) - User ID

**Response (200):**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com"
}
```

**Error Response (404):**
```json
{
  "error": "User not found"
}
```

#### Create User
```http
POST /api/users/
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "New User",
  "email": "newuser@example.com"
}
```

**Response (201):**
```json
{
  "id": 3,
  "name": "New User",
  "email": "newuser@example.com"
}
```

**Error Responses:**
- `400` - Missing required fields
- `409` - Email already exists

#### Update User
```http
PUT /api/users/{id}
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Updated Name",
  "email": "updated@example.com"
}
```

**Response (200):**
```json
{
  "id": 1,
  "name": "Updated Name",
  "email": "updated@example.com"
}
```

**Error Responses:**
- `400` - Invalid request data
- `404` - User not found
- `409` - Email already exists

#### Delete User
```http
DELETE /api/users/{id}
```

**Response (204):** No content

**Error Response (404):**
```json
{
  "error": "User not found"
}
```

**Note:** Deleting a user will also delete all their posts.

### Posts Endpoints

#### Get All Posts
```http
GET /api/posts/
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "First Post",
    "content": "This is the content of the first post",
    "user_id": 1
  },
  {
    "id": 2,
    "title": "Second Post",
    "content": "This is the content of the second post",
    "user_id": 2
  }
]
```

#### Get Post by ID
```http
GET /api/posts/{id}
```

**Parameters:**
- `id` (integer) - Post ID

**Response (200):**
```json
{
  "id": 1,
  "title": "First Post",
  "content": "This is the content of the first post",
  "user_id": 1
}
```

**Error Response (404):**
```json
{
  "error": "Post not found"
}
```

#### Create Post
```http
POST /api/posts/
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "New Post",
  "content": "This is the content of the new post",
  "user_id": 1
}
```

**Response (201):**
```json
{
  "id": 4,
  "title": "New Post",
  "content": "This is the content of the new post",
  "user_id": 1
}
```

**Error Responses:**
- `400` - Missing required fields
- `404` - User not found (invalid user_id)

#### Update Post
```http
PUT /api/posts/{id}
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "Updated Post Title",
  "content": "Updated content",
  "user_id": 2
}
```

**Response (200):**
```json
{
  "id": 1,
  "title": "Updated Post Title",
  "content": "Updated content",
  "user_id": 2
}
```

**Error Responses:**
- `400` - Invalid request data
- `404` - Post not found or user not found

#### Delete Post
```http
DELETE /api/posts/{id}
```

**Response (204):** No content

**Error Response (404):**
```json
{
  "error": "Post not found"
}
```

#### Get Posts by User
```http
GET /api/posts/user/{user_id}
```

**Parameters:**
- `user_id` (integer) - User ID

**Response (200):**
```json
[
  {
    "id": 1,
    "title": "First Post",
    "content": "This is the content of the first post",
    "user_id": 1
  },
  {
    "id": 3,
    "title": "Third Post",
    "content": "This is the content of the third post",
    "user_id": 1
  }
]
```

**Error Response (404):**
```json
{
  "error": "User not found"
}
```

## Testing

### Running Tests

1. **Run all tests**
   ```bash
   python -m pytest
   ```

2. **Run tests with verbose output**
   ```bash
   python -m pytest -v
   ```

3. **Run specific test files**
   ```bash
   python -m pytest tests/test_users.py
   python -m pytest tests/test_posts.py
   python -m pytest tests/test_data_store.py
   python -m pytest tests/test_integration.py
   ```

4. **Run tests with coverage**
   ```bash
   python -m pytest --cov=.
   ```

### Test Coverage

The test suite includes:
- **59 total tests** covering all endpoints and functionality
- **Unit tests** for data store operations
- **Integration tests** for complete API workflows
- **Error handling tests** for all error scenarios
- **Data validation tests** for input validation

### Test Categories

1. **Data Store Tests** (20 tests)
   - User and Post class functionality
   - CRUD operations
   - Data validation and integrity

2. **Users Endpoint Tests** (16 tests)
   - All HTTP methods (GET, POST, PUT, DELETE)
   - Validation and error handling
   - Cascade deletion behavior

3. **Posts Endpoint Tests** (18 tests)
   - All HTTP methods
   - User ID validation
   - Error scenarios

4. **Integration Tests** (5 tests)
   - Complete workflows
   - Data consistency
   - Error handling scenarios

## Project Structure

```
rest-api/
├── app.py                 # Main Flask application
├── users.py              # Users Blueprint
├── posts.py              # Posts Blueprint
├── data_store.py         # In-memory data store
├── conftest.py           # Test configuration
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── ARCHITECTURE.md      # Architecture documentation
└── tests/               # Test files
    ├── test_users.py
    ├── test_posts.py
    ├── test_data_store.py
    └── test_integration.py
```

## Example Usage

### Using curl

```bash
# Get all users
curl http://localhost:5000/api/users/

# Create a new user
curl -X POST http://localhost:5000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User", "email": "test@example.com"}'

# Get a specific user
curl http://localhost:5000/api/users/1

# Update a user
curl -X PUT http://localhost:5000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Name"}'

# Delete a user
curl -X DELETE http://localhost:5000/api/users/1

# Create a post
curl -X POST http://localhost:5000/api/posts/ \
  -H "Content-Type: application/json" \
  -d '{"title": "My Post", "content": "Post content", "user_id": 1}'

# Get posts by user
curl http://localhost:5000/api/posts/user/1
```

### Using Python requests

```python
import requests

base_url = "http://localhost:5000/api"

# Create a user
user_data = {"name": "Python User", "email": "python@example.com"}
response = requests.post(f"{base_url}/users/", json=user_data)
user = response.json()

# Create a post for the user
post_data = {
    "title": "Python Post",
    "content": "Created via Python",
    "user_id": user["id"]
}
response = requests.post(f"{base_url}/posts/", json=post_data)
post = response.json()

print(f"Created user: {user['name']}")
print(f"Created post: {post['title']}")
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).