import routers
from app import app
from routers import cron, deprecated, livers, users

app.include_router(routers.router)
app.include_router(livers.router)
app.include_router(users.router)
app.include_router(cron.router)
app.include_router(deprecated.router)
