import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler
from asgi_correlation_id import CorrelationIdMiddleware
from social_api.routers.post import router as post_router
from social_api.routers.user import router as user_router
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
app.add_middleware(CorrelationIdMiddleware)

# app.include_router(post_router, prefix="posts")
app.include_router(post_router)
app.include_router(user_router)


@app.exception_handler(HTTPException)
async def http_exception_handler_logging(request, exc):
    logger.error(f"HTTPException: {exc.status_code} {exc.detail}")
    return await http_exception_handler(request, exc)
