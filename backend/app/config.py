from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "seder_user"
    DB_PASSWORD: str = "seder_pass"
    DB_NAME: str = "seder"

    JWT_SECRET: str = "supersecretkeychangeinproduction"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 480

    APP_NAME: str = "SEDER - Sistema Eclesial"
    APP_VERSION: str = "1.0.0"

    class Config:
        env_file = "../../.env"


settings = Settings()
