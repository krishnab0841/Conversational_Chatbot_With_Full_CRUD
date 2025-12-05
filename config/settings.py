"""
Configuration settings for the AI Agent Chatbot.
Loads environment variables and provides application-wide settings.
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Google Gemini API
    google_api_key: str = Field(..., alias="GOOGLE_API_KEY")
    gemini_model: str = Field(default="gemini-2.0-flash-exp", alias="GEMINI_MODEL")
    
    # PostgreSQL Database
    db_host: str = Field(default="localhost", alias="DB_HOST")
    db_port: int = Field(default=5432, alias="DB_PORT")
    db_name: str = Field(default="chatbot_db", alias="DB_NAME")
    db_user: str = Field(default="postgres", alias="DB_USER")
    db_password: str = Field(..., alias="DB_PASSWORD")
    
    # Application
    app_mode: str = Field(default="web", alias="APP_MODE")  # web or cli
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    
    # Chatbot
    max_conversation_turns: int = Field(default=50, alias="MAX_CONVERSATION_TURNS")
    temperature: float = Field(default=0.7, alias="TEMPERATURE")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    @property
    def database_url(self) -> str:
        """Generate PostgreSQL connection URL."""
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


# Global settings instance
def get_settings() -> Settings:
    """Get settings instance."""
    return Settings()
