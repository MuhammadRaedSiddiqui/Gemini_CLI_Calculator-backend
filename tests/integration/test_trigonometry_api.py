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
async def test_trig_endpoint_sin_degrees_success(client: AsyncClient):
    response = await client.post("/trigonometry/evaluate", json={
        "function": "sin",
        "value": 90,
        "unit": "degrees"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == pytest.approx(1.0)
    assert data["function"] == "sin"
    assert data["unit"] == "degrees"

async def test_trig_endpoint_acos_radians_success(client: AsyncClient):
    response = await client.post("/trigonometry/evaluate", json={
        "function": "acos",
        "value": 1,
        "unit": "radians"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == pytest.approx(0.0)

async def test_trig_endpoint_atan_degrees_success(client: AsyncClient):
    response = await client.post("/trigonometry/evaluate", json={
        "function": "atan",
        "value": 1,
        "unit": "degrees"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == pytest.approx(45.0)

async def test_trig_endpoint_sinh_success(client: AsyncClient):
    response = await client.post("/trigonometry/evaluate", json={
        "function": "sinh",
        "value": 1,
        "unit": "radians" # Unit is irrelevant for sinh but required by model
    })
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == pytest.approx(np.sinh(1))

# --- Error Cases ---
async def test_trig_endpoint_domain_error(client: AsyncClient):
    """ Test API response for an input outside the function's domain. """
    response = await client.post("/trigonometry/evaluate", json={
        "function": "asin",
        "value": 2,
        "unit": "radians"
    })
    assert response.status_code == 400
    assert "Domain error" in response.json()["detail"]

async def test_trig_endpoint_invalid_function_name(client: AsyncClient):
    """ Test API response for a function name that is not in the Enum. """
    response = await client.post("/trigonometry/evaluate", json={
        "function": "invalid_function",
        "value": 1,
        "unit": "radians"
    })
    # This should be a 422 Unprocessable Entity error due to Pydantic validation
    assert response.status_code == 422
    assert "Input should be" in response.json()["detail"][0]["msg"]

async def test_trig_endpoint_invalid_unit_name(client: AsyncClient):
    """ Test API response for a unit name that is not in the Enum. """
    response = await client.post("/trigonometry/evaluate", json={
        "function": "sin",
        "value": 1,
        "unit": "invalid_unit"
    })
    assert response.status_code == 422
    assert "Input should be" in response.json()["detail"][0]["msg"]
