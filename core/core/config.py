from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SQLAlCHEMY_DATABASE_URL: str = "sqlite:///:memory:"
    JWT_SECRET_KEY: str = "test"
    model_config = SettingsConfigDict(env_file=".env")

    SENTRY_DSN:str = "https://75b071b6160b780fac49f1bde10183d3@sentry.hamravesh.com/10409"

    REDIS_URL: str = "redis://redis:6379"

    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: str = "no-reply@example.com"
    MAIL_PORT: int = 25
    MAIL_SERVER: str = "smtp4dev"
    MAIL_FROM_NAME: str = "admin"
    MAIL_STARTTLS: bool = False
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = False


settings = Settings()
