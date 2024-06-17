from pydantic import Field

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    telegram_token: str = Field("telegram_token", env="TELEGRAM_TOKEN")
    openai_api_key: str = Field("openai_api_key", env="OPENAI_API_KEY")

    db_host: str = Field("db_host", env="DB_HOST")
    db_port: int = Field("db_port", env="DB_PORT")
    db_name: str = Field("db_name", env="DB_NAME")
    db_user: str = Field("db_user", env="DB_USER")
    db_pass: str = Field("db_pass", env="DB_PASS")

    assistant_id: str = Field("no_id", env="ASSISTANT_ID")
    value_assistant_id: str = Field("no_id", env="VALUE_ASSISTANT_ID")

    @property
    def get_database_url(self):
        return f"postgresql+asyncpg://{settings.db_user}:{settings.db_pass}@{settings.db_host}:{settings.db_port}/{settings.db_name}"

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()