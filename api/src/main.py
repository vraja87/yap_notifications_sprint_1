from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import publish
from core.config import settings


@asynccontextmanager
async def lifespan(application: FastAPI):
    yield


app = FastAPI(title=settings.PROJECT_NAME, docs_url="/api/v1/openapi", openapi_url="/api/v1/openapi.json", root_path="/", default_response_class=ORJSONResponse, lifespan=lifespan)


@app.get("/api/v1/health")
async def healthcheck():
    return {"status":"ok"}


app.include_router(publish.router, prefix="/api/v1", tags=["Publish"])
