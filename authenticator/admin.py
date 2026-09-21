from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from authenticator.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom admin for the User model."""

    list_display = ("email", "username", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    search_fields = ("email", "username")
    ordering = ("email",)
