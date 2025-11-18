from fastapi import APIRouter

from modules.catalogs import models
from modules.notification import models
from modules.users import models
from modules.orders import models

from db.database import Base

from modules.catalogs.routers import router as catalogs_router
from modules.notification.routers import router as notifications_router
from modules.users.routers import router as users_router
from modules.orders.routers import router as orders_router

router = APIRouter(prefix='api/v1/')


router.include_router(catalogs_router)
router.include_router(notifications_router)
router.include_router(users_router)
router.include_router(orders_router)
