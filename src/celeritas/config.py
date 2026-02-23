from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    celeritas_db_path: str = Field(
        default="./data/celeritas.db", validation_alias="CELERITAS_DB_PATH"
    )
    celeritas_port: int = Field(
        default=8000, validation_alias="CELERITAS_PORT"
    )
    celeritas_schedule_interval: int = Field(
        default=60, validation_alias="CELERITAS_SCHEDULE_INTERVAL"
    )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings: Settings = Settings()
