import pytest
from typing import AsyncGenerator, TYPE_CHECKING

from httpx import ASGITransport, AsyncClient
from main import app as fastapi_app

# TODO: あとで循環参照を解決する

if TYPE_CHECKING:
    from fastapi import FastAPI


@pytest.fixture
async def app() -> "FastAPI":
    """FastAPIアプリケーションのフィクスチャ"""
    return fastapi_app


@pytest.fixture
async def client(app: "FastAPI") -> AsyncGenerator[AsyncClient, None]:
    """テスト用の非同期HTTPクライアントのフィクスチャ"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
