"""
Marshmallow schemas for data validation and serialization.

This module defines schemas for User and Post models with validation rules
and custom validation for referential integrity.
"""

from marshmallow import Schema, fields, validates, ValidationError
from data_store import data_store


class UserSchema(Schema):
    """Schema for User model validation and serialization."""

    id = fields.Integer(dump_only=True, description="Unique user identifier")
    name = fields.String(required=True, allow_none=False,
                         description="User's full name")
    email = fields.Email(required=True, allow_none=False,
                         description="User's email address")

    @validates('name')
    def validate_name(self, value):
        """Validate that name is not empty or just whitespace."""
        if not value or not value.strip():
            raise ValidationError('Name cannot be empty or just whitespace.')

    @validates('email')
    def validate_email_uniqueness(self, value):
        """Validate that email is unique (excluding current user if updating)."""
        # Get the current user ID from context if available (for updates)
        current_user_id = self.context.get(
            'current_user_id') if self.context else None

        # Check if email already exists for a different user
        existing_user = data_store.get_user_by_email(value)
        if existing_user and existing_user.id != current_user_id:
            raise ValidationError('Email address already exists.')


class PostSchema(Schema):
    """Schema for Post model validation and serialization."""

    id = fields.Integer(dump_only=True, description="Unique post identifier")
    title = fields.String(required=True, allow_none=False,
                          description="Post title")
    content = fields.String(
        required=True, allow_none=False, description="Post content")
    user_id = fields.Integer(required=True, allow_none=False,
                             description="ID of the user who created the post")

    @validates('title')
    def validate_title(self, value):
        """Validate that title is not empty or just whitespace."""
        if not value or not value.strip():
            raise ValidationError('Title cannot be empty or just whitespace.')

    @validates('content')
    def validate_content(self, value):
        """Validate that content is not empty or just whitespace."""
        if not value or not value.strip():
            raise ValidationError(
                'Content cannot be empty or just whitespace.')

    @validates('user_id')
    def validate_user_id_exists(self, value):
        """Validate that the user_id exists in the database."""
        if not data_store.user_exists(value):
            raise ValidationError(
                'User with the specified user_id does not exist.')


class UserUpdateSchema(Schema):
    """Schema for User model updates (allows partial updates)."""

    name = fields.String(allow_none=False, description="User's full name")
    email = fields.Email(allow_none=False, description="User's email address")

    @validates('name')
    def validate_name(self, value):
        """Validate that name is not empty or just whitespace."""
        if value is not None and (not value or not value.strip()):
            raise ValidationError('Name cannot be empty or just whitespace.')

    @validates('email')
    def validate_email_uniqueness(self, value):
        """Validate that email is unique (excluding current user if updating)."""
        if value is not None:
            # Get the current user ID from context if available (for updates)
            current_user_id = self.context.get(
                'current_user_id') if self.context else None

            # Check if email already exists for a different user
            existing_user = data_store.get_user_by_email(value)
            if existing_user and existing_user.id != current_user_id:
                raise ValidationError('Email address already exists.')


class PostUpdateSchema(Schema):
    """Schema for Post model updates (allows partial updates)."""

    title = fields.String(allow_none=False, description="Post title")
    content = fields.String(allow_none=False, description="Post content")
    user_id = fields.Integer(
        allow_none=False, description="ID of the user who created the post")

    @validates('title')
    def validate_title(self, value):
        """Validate that title is not empty or just whitespace."""
        if value is not None and (not value or not value.strip()):
            raise ValidationError('Title cannot be empty or just whitespace.')

    @validates('content')
    def validate_content(self, value):
        """Validate that content is not empty or just whitespace."""
        if value is not None and (not value or not value.strip()):
            raise ValidationError(
                'Content cannot be empty or just whitespace.')

    @validates('user_id')
    def validate_user_id_exists(self, value):
        """Validate that the user_id exists in the database."""
        if value is not None and not data_store.user_exists(value):
            raise ValidationError(
                'User with the specified user_id does not exist.')


# Schema instances for use in routes
user_schema = UserSchema()
users_schema = UserSchema(many=True)
user_update_schema = UserUpdateSchema()

post_schema = PostSchema()
posts_schema = PostSchema(many=True)
post_update_schema = PostUpdateSchema()
