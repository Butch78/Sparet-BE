from pydantic import BaseSettings
from pydantic.fields import Field
from dotenv import load_dotenv


class Settings(BaseSettings):

    # Plaid API Settings
    PLAID_CLIENT_ID: str = Field(..., env="PLAID_CLIENT_ID")
    PLAID_SECRET: str = Field(..., env="PLAID_SECRET")

    # Postgres Settings
    POSTGRES_USER: str = None
    POSTGRES_PASSWORD: str = None
    POSTGRES_HOST: str = None
    POSTGRES_PORT: int = None
    POSTGRES_DB: str = None

    class config:
        env_file = ".env"
        case_sensitive = True
        


settings = Settings()
