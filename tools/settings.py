from pydantic import BaseSettings


class Settings(BaseSettings):
    """Override Pydantic env settings.

    Use .env variables, overridden by environment varaibles if exist.
    Add fields with specific app parameters to allow validation at startup.
    """

    # Uvicorn settings
    HOST: str = "localhost"
    PORT: int = 8000
    RELOAD: bool = True

    # FastAPI settings
    NAME = "tweesent-backend"
    DESCRIPTION = "Tweesent backend for NLP Sentiment"

    # Tweepy settings
    BEARER_TOKEN: str = ""
    CONSUMER_KEY: str = ""
    CONSUMERT_SECRET: str = ""
    ACCESS_TOKEN: str = ""
    ACCESS_TOKEN_SECRET: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
