import os
from dotenv import load_dotenv


load_dotenv()


class Settings:

    # ========= API KEYS =========

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")

    WEBHOOK_SECRET: str = os.getenv(
        "WEBHOOK_SECRET",
        "change_me"
    )

    # ========= DATABASE =========

    DATABASE_URL: str = os.getenv(

        "DATABASE_URL",

        "postgresql://postgres:postgres@localhost:5432/sentinelscan"

    )

    # ========= REDIS =========

    REDIS_URL: str = os.getenv(

        "REDIS_URL",

        "redis://localhost:6379/0"

    )

    # ========= APP SETTINGS =========

    APP_NAME: str = "SentinelScan"

    DEBUG: bool = os.getenv("DEBUG", "True") == "True"

    LOG_LEVEL: str = os.getenv(

        "LOG_LEVEL",

        "INFO"

    )

    # ========= GITHUB =========

    GITHUB_API_BASE: str = os.getenv(

        "GITHUB_API_BASE",

        "https://api.github.com"

    )

    GITHUB_DEFAULT_BRANCH: str = os.getenv(

        "GITHUB_DEFAULT_BRANCH",

        "main"

    )


settings = Settings() 