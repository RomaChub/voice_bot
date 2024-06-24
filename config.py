import os
from aiogram.fsm.storage.redis import RedisStorage
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    telegram_token: str = os.getenv("TELEGRAM_TOKEN")
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    amplitude_api_key: str = os.getenv("AMPLITUDE_API_KEY")

    db_host: str = os.getenv("DB_HOST")
    db_port: int = os.getenv("DB_PORT")
    db_name: str = os.getenv("DB_NAME")
    db_user: str = os.getenv("DB_USER")
    db_pass: str = os.getenv("DB_PASS")

    redis_host: str = os.getenv("REDIS_HOST")
    redis_port: int = os.getenv("REDIS_PORT")
    redis_db: int = os.getenv("REDIS_DB")
    redis_username: str = os.getenv("REDIS_USERNAME")
    redis_pass: str = os.getenv("REDIS_PASS")

    assistant_id: str = os.getenv("ASSISTANT_ID")
    value_assistant_id: str = os.getenv("VALUE_ASSISTANT_ID")

    postgres_volume_path: str = os.getenv("POSTGRES_VOLUME_PATH")

    @property
    def get_database_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"


settings = Settings()

storage = RedisStorage.from_url(
    f"redis://{settings.redis_username}:{settings.redis_pass}@{settings.redis_host}:{settings.redis_port}/{settings.redis_db}")
