import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database URL - defaults to SQLite for development if not set
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    # Default to SQLite for local development
    DATABASE_URL = "sqlite:///./portfolio.db"
    print("⚠️  DATABASE_URL not set, using SQLite: sqlite:///./portfolio.db")
elif DATABASE_URL.startswith("postgres://"):
    # Fix Render's DATABASE_URL for SQLAlchemy
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# JWT Secret Key - generate a default for development if not set
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
if not JWT_SECRET_KEY:
    JWT_SECRET_KEY = "dev-secret-key-change-in-production"
    print("⚠️  JWT_SECRET_KEY not set, using default (not secure for production)")

JWT_ALGORITHM = "HS256" 
