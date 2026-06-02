import os
import logging
from pathlib import Path

class Config:
    """Application configuration from environment variables"""

    # Environment
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    DEBUG = ENVIRONMENT == "development"

    # Paths
    BASE_DIR = Path(__file__).parent
    DATA_PATH = os.getenv("DATA_PATH", str(BASE_DIR / "theaters.csv"))
    LOG_DIR = BASE_DIR / "logs"

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO" if not DEBUG else "DEBUG")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Streamlit
    STREAMLIT_CONFIG = {
        "server": {
            "port": int(os.getenv("PORT", 8501)),
            "address": "0.0.0.0",
            "headless": True,
            "enableCORS": DEBUG,
            "enableXsrfProtection": not DEBUG,
        },
        "client": {
            "showErrorDetails": DEBUG,
        },
        "logger": {
            "level": LOG_LEVEL,
        },
    }

    @classmethod
    def setup_logging(cls):
        """Configure logging for the application"""
        cls.LOG_DIR.mkdir(exist_ok=True)

        # Configure root logger
        logging.basicConfig(
            level=getattr(logging, cls.LOG_LEVEL),
            format=cls.LOG_FORMAT,
            handlers=[
                logging.FileHandler(cls.LOG_DIR / "app.log"),
                logging.StreamHandler(),
            ],
        )

        return logging.getLogger(__name__)

    @classmethod
    def validate(cls):
        """Validate that required files and configurations exist"""
        errors = []

        if not Path(cls.DATA_PATH).exists():
            errors.append(f"Data file not found: {cls.DATA_PATH}")

        if errors:
            logger = logging.getLogger(__name__)
            for error in errors:
                logger.error(error)
            raise FileNotFoundError(f"Configuration validation failed: {'; '.join(errors)}")
