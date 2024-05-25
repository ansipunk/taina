import urllib.parse

import pydantic_settings


class PostgresSettings(pydantic_settings.BaseSettings):
    host: str = "127.0.0.1"
    port: int = 5432
    username: str = "taina"
    password: str = "taina"
    database: str = "taina"

    @property
    def url(self):
        password = urllib.parse.quote_plus(self.password)

        return (
            f"postgresql+psycopg://{self.username}:{password}"
            f"@{self.host}:{self.port}/{self.database}"
        )

    model_config = pydantic_settings.SettingsConfigDict(env_prefix="TAINA_POSTGRES_")


postgres = PostgresSettings()
