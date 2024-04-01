from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_DOCKER_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_DOCKER_NAME: str
    FERNET_KEY: bytes

    @property
    def async_database_url(self):
        return f"postgresql+asyncpg://" \
               f"{self.DB_USER}:{self.DB_PASS}" \
               f"@{self.DB_DOCKER_HOST}:{self.DB_PORT}" \
               f"/{self.DB_DOCKER_NAME}"

    class Config:
        env_file = ".env"
        extra = 'allow'


settings = Settings()
