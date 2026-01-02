from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    """Configurazione dell'applicazione"""
    
    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_DEBUG: bool = False
    
    # PBX Settings (OBBLIGATORI - configura in .env)
    PBX_HOST: str
    PBX_PORT: int = 5038
    PBX_USER: str
    PBX_PASSWORD: str
    
    # Application Settings
    DEFAULT_INTERNAL: str = "233"
    FRONTEND_URL: str = "http://localhost:3000"
    APP_NAME: str = "PBX Call Manager"
    APP_VERSION: str = "1.0.0"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Ignora campi extra dal file .env

settings = Settings()
