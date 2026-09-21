import uuid
from ninja import Schema
from pydantic import EmailStr, field_validator


# ── Request Schemas ──────────────────────────────────────────────


class RegisterSchema(Schema):
    """Schema for user registration."""

    email: EmailStr
    username: str
    password: str
    password_confirm: str

    @field_validator("username")
    @classmethod
    def username_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Username cannot be empty.")
        return v.strip()

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters.")
        return v


class ChangePasswordSchema(Schema):
    """Schema for changing password."""

    old_password: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def new_password_min_length(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("New password must be at least 8 characters.")
        return v


# ── Response Schemas ─────────────────────────────────────────────


class UserResponseSchema(Schema):
    """Schema for user profile responses."""

    id: uuid.UUID
    email: str
    username: str
    first_name: str
    last_name: str
    is_active: bool
    date_joined: str


class MessageSchema(Schema):
    """Generic message response."""

    message: str
