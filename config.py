from pydantic import Field

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    telegram_token: str = Field("telegram_token", env="TELEGRAM_TOKEN")
    openai_api_key: str = Field("openai_api_key", env="OPENAI_API_KEY")

    assistant_id: str = Field("no_id", env="ASSISTANT_ID")

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
