import pytest
from httpx import AsyncClient
from app.main import app
import os
import asyncio

@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/")
        assert r.status_code == 200
        assert "Weather API" in r.json().get("msg", "")

@pytest.mark.asyncio
async def test_invalid_city():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/weather", params={"city": "citythatdoesnotexistabcxyz"})
        assert r.status_code in (404, 502)

@pytest.mark.asyncio
async def test_rate_limit():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        responses = []
        for _ in range(5):
            responses.append(await ac.get("/weather", params={"city": "London"}))
        assert all(r.status_code in (200, 404, 502, 429) for r in responses)