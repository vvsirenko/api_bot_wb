from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, \
    AsyncEngine
from sqlalchemy.orm import declarative_base, sessionmaker

from sqlalchemy import select, Column, Integer, String, Float

from app import config

Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    artikul = Column(Integer, unique=True, index=True)
    name = Column(String)
    price = Column(Float)
    rating = Column(Float)
    total_quantity = Column(Integer)


async_engine: AsyncEngine = create_async_engine(
    config.DATABASE_URL, echo=True
)
AsyncSessionLocal = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await async_engine.dispose()


async def get_async_session() -> AsyncSession:
    try:
        async with AsyncSessionLocal() as session:
            yield session
    finally:
        async_engine.dispose()
