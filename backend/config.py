from pathlib import Path
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent / ".env",
        env_file_encoding="utf-8",
        env_prefix="TODO_",
        hide_input_in_errors=True,
    )

    db_host: str = "localhost"
    db_port: int = Field(default=5432, ge=1, le=65535)
    db_name: str = "todo_db"
    db_user: str = "todo_app"
    db_password: SecretStr = Field(min_length=1)
    jwt_secret: SecretStr = Field(min_length=64)

settings = Settings()