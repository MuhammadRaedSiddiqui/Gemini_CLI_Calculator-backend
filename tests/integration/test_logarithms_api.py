import pytest
from httpx import AsyncClient, ASGITransport
import numpy as np
from app.main import app

# Mark all tests in this file as asyncio
pytestmark = pytest.mark.asyncio

@pytest.fixture
async def client():
    """ Create an async test client for the app. """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

# --- Success Cases ---
async def test_log_endpoint_ln_success(client: AsyncClient):
    response = await client.post("/logarithms/evaluate", json={
        "function": "ln",
        "value": np.e**2
    })
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == pytest.approx(2.0)
    assert data["function"] == "ln"
    assert data["base"] is None

async def test_log_endpoint_log10_success(client: AsyncClient):
    response = await client.post("/logarithms/evaluate", json={
        "function": "log10",
        "value": 1000
    })
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == pytest.approx(3.0)

async def test_log_endpoint_custom_log_success(client: AsyncClient):
    response = await client.post("/logarithms/evaluate", json={
        "function": "log",
        "value": 1024,
        "base": 2
    })
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == pytest.approx(10.0)
    assert data["function"] == "log"
    assert data["base"] == 2

# --- Error Cases (caught by Pydantic validator) ---
async def test_log_endpoint_missing_base_for_log_error(client: AsyncClient):
    response = await client.post("/logarithms/evaluate", json={
        "function": "log",
        "value": 1024
        # Missing 'base'
    })
    assert response.status_code == 422  # Pydantic validation error
    assert "`base` is required" in response.json()["detail"][0]["msg"]

async def test_log_endpoint_extra_base_for_ln_error(client: AsyncClient):
    response = await client.post("/logarithms/evaluate", json={
        "function": "ln",
        "value": 10,
        "base": 2 # Extra 'base'
    })
    assert response.status_code == 422 # Pydantic validation error
    assert "`base` should not be provided" in response.json()["detail"][0]["msg"]

# --- Error Cases (caught by service layer) ---
async def test_log_endpoint_domain_error_negative_value(client: AsyncClient):
    response = await client.post("/logarithms/evaluate", json={
        "function": "ln",
        "value": -10
    })
    assert response.status_code == 400
    assert "Domain error" in response.json()["detail"]

async def test_log_endpoint_invalid_base_one(client: AsyncClient):
    response = await client.post("/logarithms/evaluate", json={
        "function": "log",
        "value": 10,
        "base": 1
    })
    assert response.status_code == 400
    assert "Logarithm base must be positive and not equal to 1" in response.json()["detail"]
