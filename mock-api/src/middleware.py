import os

from fastapi import Request, status
from fastapi.responses import ORJSONResponse


class AuthMiddleware:
    def __init__(
            self,
            app,
    ):
        pass

    async def __call__(self, request: Request, call_next):
        if request.scope["path"] != "/api/v1/health":
            token = request.headers.get("Cookie")
            if not token or not os.environ["SERVICE_TOKEN"] in token:
                return ORJSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Token invalid!"}
                )
            request_id = request.headers.get("X-Request-Id")
            if not request_id:
                return ORJSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"detail": "X-Request-Id is required"}
                )
        response = await call_next(request)
        return response
