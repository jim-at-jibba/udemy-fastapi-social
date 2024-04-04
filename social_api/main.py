import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from social_api.routers.post import router as post_router
from social_api.database import database
from social_api.logging_conf import configure_logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    logger.info("Yo")
    await database.connect()
    yield
    # this is the cleanup code
    await database.disconnect()


app = FastAPI(lifespan=lifespan)


# app.include_router(post_router, prefix="posts")
app.include_router(post_router)
