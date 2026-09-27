import os
from dotenv import load_dotenv
from pathlib import Path
import re

load_dotenv(dotenv_path=Path(__file__).parent.parent.parent / ".env")

# Secret key validation
def _validate_secret_key(key: str) -> str:
    """Validate the secret key meets security requirements."""
    if not key:
        raise ValueError("SECRET_KEY must not be empty")
    if key == "your-secret-key-change-in-production":
        raise ValueError("SECRET_KEY must not be the default/insecure placeholder value")
    if len(key) < 32:
        raise ValueError("SECRET_KEY must be at least 32 characters long")
    # Check for common weak patterns
    weak_patterns = [
        r"^secret$", r"^key$", r"^change-me$", r"^default$",
        r"^insecure$", r"^test$", r"^development-only$",
    ]
    key_lower = key.lower()
    for pattern in weak_patterns:
        if re.match(pattern, key_lower):
            raise ValueError(f"SECRET_KEY appears to be a weak/placeholder value: {key}")
    return key

class Settings:
    def _get_secret_key(self) -> str:
        key = os.getenv("SECRET_KEY")
        if not key:
            # In production, this will raise ValueError and fail startup
            # In development, we provide a warning but still allow it
            import sys
            if "pytest" in sys.modules or os.getenv("FASTAPI_ENV", "development") == "development":
                key = "dev-secret-key-change-for-production"
                print(
                    "WARNING: Using development SECRET_KEY. "
                    "Set SECRET_KEY environment variable for production.",
                    file=sys.stderr,
                )
            else:
                raise ValueError("SECRET_KEY environment variable is required")
        return _validate_secret_key(key)

    SECRET_KEY: str = property(_get_secret_key)
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/hotel_management"
    )
    BACKEND_CORS_ORIGINS: list = []
    API_V1_STR: str = "/api/v1"

    @property
    def PROJECT_NAME(self) -> str:
        return "Hotel Management System"

settings = Settings()