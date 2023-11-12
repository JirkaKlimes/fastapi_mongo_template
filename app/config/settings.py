from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str
    MONGO_INITDB_DATABASE: str

    DATABASE_URL: str

    ACCESS_TOKEN_EXPIRES_IN: int
    REFRESH_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str
    JWT_SECRET: str

    CLIENT_ORIGIN: str
    HTTPS_ONLY: bool

    class Config:
        env_file = './.env'


settings = Settings()
