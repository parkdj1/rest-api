from flask import Blueprint, jsonify, request
from data_store import data_store
from schemas import user_schema, users_schema, user_update_schema
from marshmallow import ValidationError

users_bp = Blueprint('users', __name__, url_prefix='/api/users')


@users_bp.route('/', methods=['GET'])
def get_users():
    """Get all users"""
    users = data_store.get_all_users()
    return jsonify(users_schema.dump(users))


@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a single user by ID"""
    user = data_store.get_user(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user_schema.dump(user))


@users_bp.route('/', methods=['POST'])
def create_user():
    """Create a new user"""
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    try:
        # Validate the incoming data using UserSchema
        validated_data = user_schema.load(data)
    except ValidationError as err:
        # Check if it's a duplicate email error
        if 'email' in err.messages and 'Email address already exists' in str(err.messages['email']):
            return jsonify({"error": "Email already exists"}), 409
        return jsonify({"error": "Validation failed", "details": err.messages}), 400

    new_user = data_store.create_user(
        validated_data["name"], validated_data["email"])
    return jsonify(user_schema.dump(new_user)), 201


@users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update an existing user"""
    user = data_store.get_user(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    try:
        # Validate the incoming data using UserUpdateSchema with context
        user_update_schema.context = {'current_user_id': user_id}
        validated_data = user_update_schema.load(data)
    except ValidationError as err:
        # Check if it's a duplicate email error
        if 'email' in err.messages and 'Email address already exists' in str(err.messages['email']):
            return jsonify({"error": "Email already exists"}), 409
        return jsonify({"error": "Validation failed", "details": err.messages}), 400

    updated_user = data_store.update_user(
        user_id,
        name=validated_data.get('name'),
        email=validated_data.get('email')
    )
    return jsonify(user_schema.dump(updated_user))


@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user"""
    if not data_store.delete_user(user_id):
        return jsonify({"error": "User not found"}), 404
    return '', 204
