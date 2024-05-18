from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # database
    MONGODB_URI: str
    MONGODB_DATABASE_NAME: str

    # OpenAI
    OPENAI_API_KEY: str
    MODEL_NAME: str

    class Config:
        env_file = ".env"


settings = Settings()
