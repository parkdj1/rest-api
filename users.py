from flask import Blueprint, jsonify, request

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

# Sample data for demonstration
users_data = [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
]


@users_bp.route('/', methods=['GET'])
def get_users():
    """Get all users"""
    return jsonify(users_data)


@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a single user by ID"""
    user = next((user for user in users_data if user["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)


@users_bp.route('/', methods=['POST'])
def create_user():
    """Create a new user"""
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    required_fields = ['name', 'email']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"error": f"Field '{field}' is required"}), 400

    # Check if email already exists
    if any(user['email'] == data['email'] for user in users_data):
        return jsonify({"error": "Email already exists"}), 409

    new_user = {
        "id": max([user["id"] for user in users_data], default=0) + 1,
        "name": data["name"],
        "email": data["email"]
    }

    users_data.append(new_user)
    return jsonify(new_user), 201


@users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update an existing user"""
    user = next((user for user in users_data if user["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    # Check if email is being updated and if it already exists
    if 'email' in data and data['email'] != user['email']:
        if any(u['email'] == data['email'] for u in users_data if u['id'] != user_id):
            return jsonify({"error": "Email already exists"}), 409

    # Update user fields
    for field in ['name', 'email']:
        if field in data:
            user[field] = data[field]

    return jsonify(user)


@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user"""
    user = next((user for user in users_data if user["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    users_data.remove(user)
    return '', 204
