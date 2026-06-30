"""Configuration de l'application."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Variables d'environnement et paramètres applicatifs."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "Eurocode Calculator API"
    app_version: str = "0.1.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    default_gamma_c: float = 1.5
    default_gamma_s: float = 1.0
    default_gamma_m: float = 1.15


settings = Settings()
