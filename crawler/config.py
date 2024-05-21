from pydantic_settings import BaseSettings
# from pydantic import BaseSettings


class Settings(BaseSettings):
    # database
    MONGODB_URI: str
    MONGODB_DATABASE_NAME: str

    class Config:
        env_file = ".env"


settings = Settings()
