from __future__ import annotations

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


def create_engine(database_url: str, *, echo: bool = False, role: str | None = None) -> AsyncEngine:
    if not database_url.startswith("postgresql+asyncpg://"):
        raise ValueError("P1-4 authoritative store requires postgresql+asyncpg")
    connect_args = {"server_settings": {"role": role}} if role is not None else {}
    return create_async_engine(
        database_url, echo=echo, pool_pre_ping=True, connect_args=connect_args
    )


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False)
