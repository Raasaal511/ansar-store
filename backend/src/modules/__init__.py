from fastapi import APIRouter

# Импортируем модели, чтобы они зарегистрировались в Base.metadata
# (это важно для alembic и для Base.metadata.create_all)
from .catalogs import models as catalogs_models  # noqa: F401
from .users import models as users_models  # noqa: F401
from .orders import models as orders_models  # noqa: F401
# from .notification import models as notification_models  # noqa: F401

from .catalogs.routers import router as catalogs_router
# from .notification.routers import router as notifications_router
from .users.routers import router as users_router
from .orders.routers import router as orders_router
from .auth.routers import router as auth_router


router = APIRouter(prefix="/api/v1")

router.include_router(catalogs_router)
# router.include_router(notifications_router)
router.include_router(users_router)
router.include_router(orders_router)
router.include_router(auth_router)
