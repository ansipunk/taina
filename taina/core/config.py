import urllib.parse

import pydantic_settings


class PostgresSettings(pydantic_settings.BaseSettings):
    host: str = "127.0.0.1"
    port: int = 5432
    username: str = "taina"
    password: str = "taina"
    database: str = "taina"
    force_rollback: bool = False

    @property
    def url(self):
        password = urllib.parse.quote_plus(self.password)

        return (
            f"postgresql://{self.username}:{password}"
            f"@{self.host}:{self.port}/{self.database}"
        )

    model_config = pydantic_settings.SettingsConfigDict(env_prefix="TAINA_POSTGRES_")


class RedisSettings(pydantic_settings.BaseSettings):
    host: str = "127.0.0.1"
    port: int = 6379
    username: str | None = "taina"
    password: str | None = "taina"
    db: int = 0
    force_rollback: bool = False

    @property
    def url(self):
        auth = ""

        if self.username and self.password:
            auth = f"{self.username}:{self.password}@"

        return f"redis://{auth}{self.host}:{self.port}"

    model_config = pydantic_settings.SettingsConfigDict(env_prefix="TAINA_REDIS_")


class SecuritySettings(pydantic_settings.BaseSettings):
    access_token_ttl: int = 60 * 15  # 15 minutes
    refresh_token_ttl: int = 60 * 60 * 24  # 1 day
    user_password_salt: str = "00000000000000000000000000000000"

    model_config = pydantic_settings.SettingsConfigDict(env_prefix="TAINA_SECURITY_")


postgres = PostgresSettings()
redis = RedisSettings()
security = SecuritySettings()
