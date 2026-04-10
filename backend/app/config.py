import os

from dotenv import load_dotenv


# =========================
# LOAD ENV
# =========================

load_dotenv()


def to_bool(value: str | None, default=False):

    if value is None:

        return default


    return str(value).lower() in (

        "true",

        "1",

        "yes",

        "y"

    )


def to_int(value: str | None, default=0):

    try:

        return int(value)

    except:

        return default


# =========================
# SETTINGS CLASS
# =========================

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


    ADMIN_SECRET: str = os.getenv(

        "ADMIN_SECRET",

        ""

    )


    # =========================
    # DATABASE
    # =========================

    DATABASE_URL: str = os.getenv(

        "DATABASE_URL",

        "postgresql+psycopg2://postgres:postgres@db:5432/sentinelscan"

    )


    # =========================
    # REDIS / CELERY
    # =========================

    REDIS_URL: str = os.getenv(

        "REDIS_URL",

        "redis://redis:6379/0"

    )


    CELERY_CONCURRENCY: int = to_int(

        os.getenv(

            "CELERY_CONCURRENCY"

        ),

        2

    )


    # =========================
    # AI MODEL
    # =========================

    FAST_LLM_MODEL: str = os.getenv(

        "FAST_LLM_MODEL",

        "gpt-4o-mini"

    )


    AI_TIMEOUT: int = to_int(

        os.getenv(

            "AI_TIMEOUT"

        ),

        60

    )


    AI_RETRIES: int = to_int(

        os.getenv(

            "AI_RETRIES"

        ),

        3

    )


    AI_MAX_CHARS: int = to_int(

        os.getenv(

            "AI_MAX_CHARS"

        ),

        120000

    )


    # =========================
    # APP SETTINGS
    # =========================

    APP_NAME: str = os.getenv(

        "APP_NAME",

        "SentinelScan"

    )


    DEBUG: bool = to_bool(

        os.getenv(

            "DEBUG"

        ),

        True

    )


    LOG_LEVEL: str = os.getenv(

        "LOG_LEVEL",

        "INFO"

    )


    CORS_ORIGINS: list[str] = os.getenv(

        "CORS_ORIGINS",

        "*"

    ).split(",")


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

    MAX_FILES: int = to_int(

        os.getenv(

            "MAX_FILES"

        ),

        120

    )


    MAX_FILE_SIZE_KB: int = to_int(

        os.getenv(

            "MAX_FILE_SIZE_KB"

        ),

        500

    )


    # =========================
    # WEBHOOK
    # =========================

    N8N_WEBHOOK_URL: str = os.getenv(

        "N8N_WEBHOOK_URL",

        "http://localhost:5678/webhook/scan-result"

    )


    WEBHOOK_TIMEOUT: int = to_int(

        os.getenv(

            "WEBHOOK_TIMEOUT"

        ),

        20

    )


    WEBHOOK_RETRIES: int = to_int(

        os.getenv(

            "WEBHOOK_RETRIES"

        ),

        3

    )


    # =========================
    # VALIDATION
    # =========================

    def validate(self):

        errors = []


        if not self.OPENAI_API_KEY:

            errors.append(

                "OPENAI_API_KEY missing"

            )


        if not self.DATABASE_URL:

            errors.append(

                "DATABASE_URL missing"

            )


        if not self.REDIS_URL:

            errors.append(

                "REDIS_URL missing"

            )


        if errors:

            raise ValueError(

                " | ".join(errors)

            )


        return True


# =========================
# SINGLETON INSTANCE
# =========================

settings = Settings()


# =========================
# VALIDATE CONFIG
# =========================

try:

    settings.validate()

except Exception as e:

    print(

        f"[CONFIG ERROR] {e}"

    )    