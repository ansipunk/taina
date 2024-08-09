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


class SecuritySettings(pydantic_settings.BaseSettings):
    secret_key: str = "0000000000000000000000000000000000000000000000000000000000000000"
    access_token_ttl: int = 30  # Minutes
    user_password_salt: str = "00000000000000000000000000000000"

    model_config = pydantic_settings.SettingsConfigDict(env_prefix="TAINA_SECURITY_")


postgres = PostgresSettings()
security = SecuritySettings()
