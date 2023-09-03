from fastapi import FastAPI

from config.db import db
from config.config import config
import logging

from views.task import task_api

logger = logging.getLogger(__name__)


def init_app():
    app = FastAPI(
        title="Task Management App",
        description="Handling Out Task",
        version="1"
    )

    @app.on_event("startup")
    def startup():
        db.connect(config.DB_CONFIG)

    @app.on_event("shutdown")
    async def shutdown():
        await db.disconnect()

    app.include_router(
        task_api,
        prefix="/api"
    )

    return app


app = init_app()

