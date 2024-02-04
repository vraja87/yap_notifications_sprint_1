import os
from pathlib import Path

from pydantic import BaseSettings

env_path = Path("..") / ".env"
env_file = env_path


class Settings(BaseSettings):
    project_name: str = "NOTIFICATIONS"


class AuthjwtSettings(BaseSettings):
    authjwt_secret_key: str = os.getenv("AUTHJWT_SECRET_KEY", "secret")
    authjwt_token_location: set = {"cookies"}
    authjwt_refresh_cookie_key = "refresh_token"
    authjwt_access_cookie_key = "access_token"
    authjwt_access_token_expires: int = 3600  # seconds
    authjwt_cookie_csrf_protect: bool = False


settings = Settings()
