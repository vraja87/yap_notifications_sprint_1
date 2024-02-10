import random

from datetime import datetime
from uuid import UUID

from fastapi import FastAPI, Request, Depends
from fastapi.responses import ORJSONResponse

from core.config import settings
from middleware import AuthMiddleware

from mock_data import users, films

app = FastAPI(
    title=settings.project_name,
    docs_url="/api/v1/openapi",
    openapi_url="/api/v1/openapi.json",
    default_response_class=ORJSONResponse,
)

auth_middleware = AuthMiddleware(app)
app.middleware("http")(auth_middleware)


def paginate(items: list, page: int = 1) -> list[dict]:
    result = items[(page-1)*50:page*50]
    return {
        "items": result,
        "total": len(result),
        "page": page,
        "size": 50,
        "pages": len(items)//50+1 - 1 + int(bool(50 % 49))
    }


@app.get("/api/v1/health")
async def healthcheck(
):
    return {"status": "ok"}


# MOCK API FOR SUMMARY
@app.get("/ugc/v1/summary")
async def ugc_summary(user_id: UUID, since: datetime):
    return {
        "new_likes": random.randrange(0, 120),
    }


# MOCK API FOR CONTENT
@app.get("/content/v1/summary")
async def content_summary(user_id: UUID):
    return random.choices(
        films, k=random.randrange(1, 10))


# MOCK API FOR AUTH
@app.get("/auth/v1/users")
async def auth_users(page: int = 1):
    return paginate(users, page)


@app.get("/auth/v1/users/users_by_group")
async def auth_users_by_group(group_id: UUID):
    return paginate([i["id"] for i in random.choices(
        users, k=random.randrange(0, 50))])
