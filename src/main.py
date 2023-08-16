from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis

from sqladmin import Admin

from api.routers import all_routers
from api.views import all_views
from db.db import engine

app = FastAPI(title="EpicCakes")

for router in all_routers:
    app.include_router(router)

admin = Admin(app, engine, title='EpicCakes Admin Panel')

for view in all_views:
    admin.add_view(view)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
