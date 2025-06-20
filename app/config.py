import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Core App Settings
APP_NAME = os.getenv("APP_NAME", "deleteMe")
APP_AUTHOR = os.getenv("APP_AUTHOR", "DarkVeilSecurity")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
PORT = int(os.getenv("PORT", 8000))

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "you-should-change-this")

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./deleteMe.db")

# Email (optional for future use)
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

