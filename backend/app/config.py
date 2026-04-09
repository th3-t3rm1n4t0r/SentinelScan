import os
from dotenv import load_dotenv


# load .env file
load_dotenv()


class Settings:

    # =========================
    # API KEYS
    # =========================

    OPENAI_API_KEY: str = os.getenv(
        "OPENAI_API_KEY",
        ""
    )

    GITHUB_TOKEN: str = os.getenv(
        "GITHUB_TOKEN",
        ""
    )

    WEBHOOK_SECRET: str = os.getenv(
        "WEBHOOK_SECRET",
        "change_me"
    )


    # =========================
    # DATABASE
    # =========================

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@db:5432/sentinelscan"
    )


    # =========================
    # REDIS / CELERY
    # =========================

    REDIS_URL: str = os.getenv(
        "REDIS_URL",
        "redis://redis:6379/0"
    )


    # =========================
    # AI MODEL
    # =========================

    FAST_LLM_MODEL: str = os.getenv(
        "FAST_LLM_MODEL",
        "gpt-4o-mini"
    )


    # =========================
    # APP SETTINGS
    # =========================

    APP_NAME: str = os.getenv(
        "APP_NAME",
        "SentinelScan"
    )

    DEBUG: bool = os.getenv(
        "DEBUG",
        "true"
    ).lower() in ["true", "1", "yes"]

    LOG_LEVEL: str = os.getenv(
        "LOG_LEVEL",
        "INFO"
    )


    # =========================
    # GITHUB
    # =========================

    GITHUB_API_BASE: str = os.getenv(
        "GITHUB_API_BASE",
        "https://api.github.com"
    )

    GITHUB_DEFAULT_BRANCH: str = os.getenv(
        "GITHUB_DEFAULT_BRANCH",
        "main"
    )


    # =========================
    # SECURITY LIMITS
    # =========================

    MAX_FILES: int = int(
        os.getenv(
            "MAX_FILES",
            "120"
        )
    )

    MAX_FILE_SIZE_KB: int = int(
        os.getenv(
            "MAX_FILE_SIZE_KB",
            "500"
        )
    )


    # =========================
    # VALIDATION
    # =========================

    def validate(self):

        if not self.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY missing in .env"
            )

        return True


# singleton
settings = Settings()


# optional validation
try:

    settings.validate()

except Exception as e:

    print(
        f"[CONFIG ERROR] {e}"
    ) 
     