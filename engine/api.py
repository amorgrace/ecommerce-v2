from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController

from authenticator.router import router as auth_router

api = NinjaExtraAPI(
    title="E-Commerce API",
    version="1.0.0",
    description="E-Commerce platform API with JWT authentication.",
)

# Register built-in JWT endpoints (token/pair, token/refresh, token/verify)
api.register_controllers(NinjaJWTDefaultController)

# Register custom auth routes
api.add_router("/auth", auth_router)
