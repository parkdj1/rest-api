from flask import Blueprint, jsonify, request
from data_store import data_store

users_bp = Blueprint('users', __name__, url_prefix='/api/users')


@users_bp.route('/', methods=['GET'])
def get_users():
    """Get all users"""
    users = data_store.get_all_users()
    return jsonify([user.to_dict() for user in users])


@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a single user by ID"""
    user = data_store.get_user(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict())


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
    existing_user = data_store.get_user_by_email(data['email'])
    if existing_user:
        return jsonify({"error": "Email already exists"}), 409

    new_user = data_store.create_user(data["name"], data["email"])
    return jsonify(new_user.to_dict()), 201


@users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update an existing user"""
    user = data_store.get_user(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    # Check if email is being updated and if it already exists
    if 'email' in data and data['email'] != user.email:
        existing_user = data_store.get_user_by_email(data['email'])
        if existing_user:
            return jsonify({"error": "Email already exists"}), 409

    updated_user = data_store.update_user(
        user_id,
        name=data.get('name'),
        email=data.get('email')
    )
    return jsonify(updated_user.to_dict())


@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user"""
    if not data_store.delete_user(user_id):
        return jsonify({"error": "User not found"}), 404
    return '', 204
