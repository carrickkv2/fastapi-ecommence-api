import pytest_asyncio
from app.core.common import get_current_user
from app.core.config import Settings
from app.db import models
from app.db.connect import get_session
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlmodel import SQLModel


DATABASE_URL = Settings().TEST_DB_CONFIG


engine = create_async_engine(DATABASE_URL, echo=True, future=True, poolclass=NullPool)


async def session():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


@pytest_asyncio.fixture
async def test_app():
    """
    Pytest fixture to create a test client.
    """
    await session()

    async def get_session_override():
        async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        async with async_session() as session:
            yield session

    def skip_auth():
        ...

    app.dependency_overrides[get_session] = get_session_override

    app.dependency_overrides[get_current_user] = skip_auth

    with TestClient(app) as client:
        yield client
