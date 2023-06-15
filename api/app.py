import os
from datetime import datetime

from fastapi import FastAPI

app = FastAPI(
    title="AI+CRYPTO HACKATHON API",
    version="v{:%Y%m%d}".format(datetime.now()),
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)
