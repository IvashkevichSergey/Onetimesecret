from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)
from app.config import settings
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(settings.async_database_url)
async_session_maker = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    """Base class to create any declarative class definitions"""
    pass


async def get_session() -> AsyncSession:
    """Generator for creating async session with the database"""
    async with async_session_maker() as session:
        yield session
