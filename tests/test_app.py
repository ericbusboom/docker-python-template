"""Tests for the FastAPI application."""

import pytest


@pytest.mark.asyncio
async def test_health(client):
    response = await client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_home_page(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert "Python App Template" in response.text
    assert "counter" in response.text.lower()


@pytest.mark.asyncio
async def test_increment_counter(client):
    """Incrementing the counter returns updated HTML partial."""
    response = await client.post("/api/counter/increment")
    assert response.status_code == 200
    # Should return the counter partial HTML
    assert "counter-widget" in response.text
    assert "counter-value" in response.text


@pytest.mark.asyncio
async def test_increment_increases_value(client):
    """Counter value increases on each increment call."""
    r1 = await client.post("/api/counter/increment")
    r2 = await client.post("/api/counter/increment")
    assert r1.status_code == 200
    assert r2.status_code == 200
    # The two responses should be different (value changed)
    assert r1.text != r2.text


@pytest.mark.asyncio
async def test_reset_counter(client):
    """Reset returns a partial with value 0."""
    # Increment first
    await client.post("/api/counter/increment")
    await client.post("/api/counter/increment")

    # Reset
    response = await client.post("/api/counter/reset")
    assert response.status_code == 200
    assert ">0<" in response.text or ">0 <" in response.text or "0</span>" in response.text


@pytest.mark.asyncio
async def test_get_counter_value(client):
    response = await client.get("/api/counter/value")
    assert response.status_code == 200
    assert "counter-widget" in response.text
