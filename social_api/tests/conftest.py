from typing import AsyncGenerator, Generator


import os
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

os.environ["ENV_STATE"] = "test"
from social_api.database import database  # noqa: E402
from social_api.main import app  # noqa: E402


# scope="session" means this will only run once
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture()
def client() -> Generator:
    yield TestClient(app)


@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    await database.connect()
    yield
    # because we have roll back set in env we will reset db on disconnect
    await database.disconnect()


# the client param is injected by pytest automatically.
# It will use the client fixture above
@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        yield ac
