from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.config import settings
from core.logger import logger


@asynccontextmanager
async def lifespan(application: FastAPI):
    yield


app = FastAPI(title=settings.project_name, docs_url="/api/v1/openapi", openapi_url="/api/v1/openapi.json", root_path="/api/", default_response_class=ORJSONResponse, lifespan=lifespan)


@app.get("/api/v1/health")
async def healthcheck():
    return {"status":"ok"}
