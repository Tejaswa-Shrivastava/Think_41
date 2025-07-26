"""
Configuration settings for the Conversational AI Backend
"""
import os
from typing import Optional

class Settings:
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/conversational_ai")
    
    # xAI API settings (using XAI_API_KEY environment variable)
    GROQ_API_KEY: str = os.getenv("XAI_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "grok-2-1212")
    
    # Application settings
    APP_NAME: str = "Conversational AI Backend"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

settings = Settings()
