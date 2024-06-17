import os

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    telegram_token: str = Field(os.getenv("TELEGRAM_TOKEN"))
    openai_api_key: str = Field(os.getenv("OPENAI_API_KEY"))

    db_host: str = Field(os.getenv("DB_HOST"))
    db_port: int = Field(os.getenv("DB_PORT"))
    db_name: str = Field(os.getenv("DB_NAME"))
    db_user: str = Field(os.getenv("DB_USER"))
    db_pass: str = Field(os.getenv("DB_PASS"))

    assistant_id: str = Field(os.getenv("ASSISTANT_ID"))
    value_assistant_id: str = Field(os.getenv("VALUE_ASSISTANT_ID"))

    postgres_volume_path: str = Field(os.getenv("POSTGRES_VOLUME_PATH"))

    @property
    def get_database_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"


settings = Settings()
