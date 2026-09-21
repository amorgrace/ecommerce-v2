from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.template.loader import render_to_string

from authenticator.email_service import send_email_via_sendlib
from authenticator.schemas import RegisterSchema, ChangePasswordSchema

if TYPE_CHECKING:
    from authenticator.models import User
else:
    User = get_user_model()

logger = logging.getLogger(__name__)


class AuthService:
    """Business logic for authentication operations."""

    @staticmethod
    def register_user(data: RegisterSchema) -> User:
        """Create a new user account and send a welcome email."""

        if data.password != data.password_confirm:
            raise ValueError("Passwords do not match.")

        if User.objects.filter(email=data.email).exists():
            raise ValueError("A user with this email already exists.")

        if User.objects.filter(username=data.username).exists():
            raise ValueError("A user with this username already exists.")

        user = User.objects.create_user(
            username=data.username,
            email=data.email,
            password=data.password,
        )

        # Send welcome email — never block registration on email failure
        try:
            explore_url = "https://blissbyuddy.com/products"
            html_content = render_to_string(
                "emails/welcome.html",
                {
                    "username": user.username,
                    "explore_url": explore_url,
                },
            )
            send_email_via_sendlib(
                to=user.email,
                subject="Welcome to BlissByUddy ✨",
                html=html_content,
                text=f"Welcome to BlissByUddy, {user.username}! Explore our products at {explore_url}",
            )
        except Exception as e:
            logger.warning(f"Welcome email failed for {user.email}: {e}")

        return user

    @staticmethod
    def change_password(user: User, data: ChangePasswordSchema) -> None:
        """Change the user's password after verifying the old one."""

        if not user.check_password(data.old_password):
            raise ValueError("Old password is incorrect.")

        if data.old_password == data.new_password:
            raise ValueError("New password must be different from the old password.")

        user.set_password(data.new_password)
        user.save(update_fields=["password"])


