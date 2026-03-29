"""Configuration and settings for the application."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    app_name: str = "Sprync Restaurant Bot"
    app_version: str = "1.0.0"
    debug: bool = False
    api_prefix: str = "/api"
    restaurant_name: str = "The Golden Plate"
    restaurant_hours: str = "11:00 AM - 11:00 PM (Daily)"
    restaurant_phone: str = "+44 20 1234 5678"
    min_party_size: int = 1
    max_party_size: int = 20
    booking_advance_days: int = 30
    frontend_path: str = "../frontend"

    class Config:
        """Pydantic config."""

        env_file = ".env"
        case_sensitive = False


settings = Settings()
