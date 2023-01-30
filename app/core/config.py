import logging

from pydantic import BaseSettings


log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    """
    A class to store all the configuration variables for the API.
    Variables are loaded automatically from the environment if they are available.
    """

    log.info("Loading config settings from the environment...")

    API_VERSION: str = "/api/v1"
    PATH_TO_INITIAL_DATA: str = "./app/data/intial_product_data.json"

    JWT_SECRET: str = "f700720f9b4a44006a2f29e7e44ad3e2ba62b31864d1e9fa70d3310668dfdacc"  # DO NOT USE THIS IN PRODUCTION - CHANGE IT
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "changeme"
    POSTGRES_DB: str = "postgres"
    DB_HOST: str = "db"
    DB_CONFIG = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}/{POSTGRES_DB}"
    TEST_DB_CONFIG = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}/test"
