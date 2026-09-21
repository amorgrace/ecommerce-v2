from ninja import Router
from ninja_jwt.authentication import JWTAuth

from authenticator.schemas import (
    ChangePasswordSchema,
    MessageSchema,
    RegisterSchema,
    UserResponseSchema,
)
from authenticator.services import AuthService

router = Router(tags=["Auth"])


# ── Public Endpoints ─────────────────────────────────────────────


@router.post("/register", response={201: UserResponseSchema, 400: MessageSchema})
def register(request, data: RegisterSchema):
    """Register a new user account."""
    try:
        user = AuthService.register_user(data)
        return 201, user
    except ValueError as e:
        return 400, {"message": str(e)}


# ── Protected Endpoints ──────────────────────────────────────────


@router.get("/me", auth=JWTAuth(), response=UserResponseSchema)
def me(request):
    """Get the current authenticated user's profile."""
    return request.auth


@router.post(
    "/change-password",
    auth=JWTAuth(),
    response={200: MessageSchema, 400: MessageSchema},
)
def change_password(request, data: ChangePasswordSchema):
    """Change the authenticated user's password."""
    try:
        AuthService.change_password(request.auth, data)
        return 200, {"message": "Password changed successfully."}
    except ValueError as e:
        return 400, {"message": str(e)}
