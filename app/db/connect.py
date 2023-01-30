import json
from pathlib import Path
from typing import AsyncGenerator

from app.core.config import Settings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlmodel import SQLModel

from . import models


DATABASE_URL = Settings().DB_CONFIG

engine = create_async_engine(DATABASE_URL, echo=True, future=True, poolclass=NullPool)


async def initialize_db_and_tables():
    """
    Creates the database and tables if they don't exist.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator:
    """
    Creates a new database session.
    """
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


async def add_initial_data_to_db(path: str):

    """
    Adds initial data to the database.
    """

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:

        current_path = Path(path).absolute()

        query = select(models.Products).where(models.Products.title == "Apple iPhone 11 Pro Max")
        results = await session.execute(query)
        product = results.scalars().first()
        if not product:
            # Add initial data to the database
            with open(current_path) as f:
                data = json.load(f)
                for product in data:
                    current_product = models.Products(**product)
                    session.add(current_product)
                    await session.commit()
                    await session.refresh(current_product)
