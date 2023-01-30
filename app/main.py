import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import Settings
from .db.connect import add_initial_data_to_db
from .db.connect import initialize_db_and_tables
from .server.api_v1.endpoints import healthcheck
from .server.api_v1.routers import api_router


log = logging.getLogger("uvicorn")


origins = [
    "http://localhost:8080",
    "http://localhost:8000",
]


def create_application() -> FastAPI:
    """
    Creates the FastAPI application with all the routes and middleware.
    """
    application = FastAPI(
        title="Test E-commerce API",
        description="""A test API created for an e-commence store.
        """,
        version="v1",
    )

    # Add CORS middleware to allow requests from the frontend
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add the routers to the application with their respective routes
    application.include_router(healthcheck.router)
    application.include_router(api_router, prefix=Settings().API_VERSION)
    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    await initialize_db_and_tables()
    await add_initial_data_to_db(Settings().PATH_TO_INITIAL_DATA)


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
