from flask import Blueprint, jsonify, request
from data_store import data_store
from schemas import post_schema, posts_schema, post_update_schema
from marshmallow import ValidationError

posts_bp = Blueprint('posts', __name__, url_prefix='/api/posts')


@posts_bp.route('/', methods=['GET'])
def get_posts():
    """Get all posts"""
    posts = data_store.get_all_posts()
    return jsonify(posts_schema.dump(posts))


@posts_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Get a single post by ID"""
    post = data_store.get_post(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    return jsonify(post_schema.dump(post))


@posts_bp.route('/', methods=['POST'])
def create_post():
    """Create a new post with user ID validation"""
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    try:
        # Validate the incoming data using PostSchema
        validated_data = post_schema.load(data)
    except ValidationError as err:
        # Check if it's an invalid user_id error
        if 'user_id' in err.messages and 'User with the specified user_id does not exist' in str(err.messages['user_id']):
            return jsonify({"error": "User not found"}), 404
        return jsonify({"error": "Validation failed", "details": err.messages}), 400

    new_post = data_store.create_post(
        validated_data["title"], validated_data["content"], validated_data["user_id"])
    return jsonify(post_schema.dump(new_post)), 201


@posts_bp.route('/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """Update an existing post"""
    post = data_store.get_post(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    try:
        # Validate the incoming data using PostUpdateSchema
        validated_data = post_update_schema.load(data)
    except ValidationError as err:
        # Check if it's an invalid user_id error
        if 'user_id' in err.messages and 'User with the specified user_id does not exist' in str(err.messages['user_id']):
            return jsonify({"error": "User not found"}), 404
        return jsonify({"error": "Validation failed", "details": err.messages}), 400

    updated_post = data_store.update_post(
        post_id,
        title=validated_data.get('title'),
        content=validated_data.get('content'),
        user_id=validated_data.get('user_id')
    )

    return jsonify(post_schema.dump(updated_post))


@posts_bp.route('/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Delete a post"""
    if not data_store.delete_post(post_id):
        return jsonify({"error": "Post not found"}), 404
    return '', 204


@posts_bp.route('/user/<int:user_id>', methods=['GET'])
def get_posts_by_user(user_id):
    """Get all posts by a specific user"""
    if not data_store.user_exists(user_id):
        return jsonify({"error": "User not found"}), 404

    user_posts = data_store.get_posts_by_user(user_id)
    return jsonify(posts_schema.dump(user_posts))
