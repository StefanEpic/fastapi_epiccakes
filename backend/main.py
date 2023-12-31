import sentry_sdk

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from prometheus_fastapi_instrumentator import Instrumentator

from redis import asyncio as aioredis

from sqladmin import Admin

from api.routers import all_routers
from api.sqladmin.views import all_views, authentication_backend
from config import SENTRY_TOKEN
from db.db import engine

sentry_sdk.init(dsn=SENTRY_TOKEN, traces_sample_rate=1.0, )

app = FastAPI(title="EpicCakes")

for router in all_routers:
    app.include_router(router)

admin = Admin(app, engine, title='EpicCakes Admin Panel', authentication_backend=authentication_backend)

for view in all_views:
    admin.add_view(view)

origins = [
    "http://localhost:80",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

Instrumentator().instrument(app).expose(app)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://redis")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
