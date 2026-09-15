"""Disposable per-case databases on the explicitly supplied test PostgreSQL."""

import asyncio
import os
import subprocess
import sys
from uuid import uuid4

import pytest
from sqlalchemy import text
from sqlalchemy.engine import make_url

from aiscc.persistence.database import create_engine


@pytest.fixture
def l2_url():
    base = make_url(os.environ["AISCC_TEST_DATABASE_URL"])
    assert base.host == "127.0.0.1"  # Never provision against a remote/private DB.
    name = "aiscc_l2_" + uuid4().hex

    async def command(sql):
        engine = create_engine(base.set(database="postgres").render_as_string(hide_password=False))
        try:
            async with engine.connect() as c:
                c = await c.execution_options(isolation_level="AUTOCOMMIT")
                await c.execute(text(sql))
        finally:
            await engine.dispose()

    asyncio.run(command('CREATE DATABASE "' + name + '"'))
    url = base.set(database=name).render_as_string(hide_password=False)
    try:
        result = subprocess.run(
            [sys.executable, "-B", "-m", "alembic", "upgrade", "head"],
            env=os.environ | {"AISCC_DATABASE_URL": url, "PYTHONDONTWRITEBYTECODE": "1"},
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr.replace(url, "<TEST_DB>")
        yield url
    finally:
        asyncio.run(command('DROP DATABASE "' + name + '"'))
