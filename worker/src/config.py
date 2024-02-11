from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

env_path = Path("../..") / ".env"
env_file = env_path


class Settings(BaseSettings):
    mock_x_request_id: str = "123"

    dead_letter_max_retries: int = 3
    dead_letter_sleep_delay: int = 300


class Service(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_file, env_prefix="SERVICE_")

    token: str = "token"


class RabbitMQ(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_file, env_prefix="RABBITMQ_")

    host: str = "localhost"
    user: str = "admin"
    password: str = "admin"
    port: str = 5672
    uri: str = f"amqp://{user}:{password}@{host}:port"

    log_queue: str = "smtp.v1.success_sent_log"
    log_ttl: int = 86400000  # 24 часа ttl


class SmtpMail(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_file, env_prefix="SMTP_")

    domain: str = "yandex.ru"
    host: str = "smtp.yandex.ru"
    port: int = 465

    login: str = "admin"
    password: str = "admin"

    real_send: bool = False


class NotifyDbSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_file, env_prefix="NOTIFY_")

    db_host: str = "notify_db"
    db_port: str = "5432"
    db_name: str = "notify"
    db_user: str = "notify"
    db_password: str = "notify"

    dsn: str = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


config_rabbit = RabbitMQ()
config_mail = SmtpMail()
config_notify_db = NotifyDbSettings()
settings = Settings()
conf_service = Service()
