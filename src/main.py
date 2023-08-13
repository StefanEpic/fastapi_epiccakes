from fastapi import FastAPI

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
