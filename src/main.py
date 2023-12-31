__import__("os").environ["TZ"] = "UTC"

import sys
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import sentry_sdk
from fastapi import FastAPI
from redis import asyncio as aioredis
from starlette.middleware.cors import CORSMiddleware

from src import redis

# from src.auth.router import router as auth_router
from src.config import app_configs, settings
from src.database import database
from src.info_user.router import router as info_user_router

# from src.hello_word.router import router as hello_word_router
from src.auth.router import router as register_router

app = FastAPI(**app_configs)


@app.on_event("startup")
async def lifespan():
    # Startup
    pool = aioredis.ConnectionPool.from_url(
        settings.REDIS_URL, max_connections=10, decode_responses=True
    )
    redis.redis_client = aioredis.Redis(connection_pool=pool)
    database.get_collection("test")


@app.on_event("shutdown")
async def shutdown():
    # Shutdown
    # await database.disconnect()
    await redis.redis_client.close()


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=settings.CORS_HEADERS,
)

if settings.ENVIRONMENT.is_deployed:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
    )


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


# app.include_router(auth_router, prefix="/auth", tags=["Auth"])


# app.include_router(
#     hello_word_router,
#     prefix="/hello_word",
# )


app.include_router(
    register_router,
    prefix="/auth",
)

app.include_router(
    info_user_router,
    prefix="/info_user",
)
