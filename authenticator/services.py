from django.contrib.auth import get_user_model

from authenticator.schemas import RegisterSchema, ChangePasswordSchema

User = get_user_model()


class AuthService:
    """Business logic for authentication operations."""

    @staticmethod
    def register_user(data: RegisterSchema) -> User:
        """Create a new user account."""

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
