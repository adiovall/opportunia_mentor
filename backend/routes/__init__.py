from .auth import router as auth_router
from .admin import router as admin_router
from .course import router as course_router
from .user import router as user_router
from .verify import router as verify_router

__all__ = ["auth_router", "admin_router", "course_router", "user_router", "verify_router"]