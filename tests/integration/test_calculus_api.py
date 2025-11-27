import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
import numpy as np

pytestmark = pytest.mark.asyncio

@pytest.fixture
async def client():
    """ Create an async test client for the app. """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

# --- Success Cases ---
async def test_calculus_endpoint_differentiate_success(client: AsyncClient):
    response = await client.post("/calculus/evaluate", json={
        "expression": "x**3 + sin(x)",
        "operation": "differentiate"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == "3*x**2 + cos(x)"
    assert data["operation"] == "differentiate"
    assert not data["is_definite_integral"]

async def test_calculus_endpoint_indefinite_integral_success(client: AsyncClient):
    response = await client.post("/calculus/evaluate", json={
        "expression": "cos(x)",
        "operation": "integrate"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == "sin(x)"
    assert not data["is_definite_integral"]

async def test_calculus_endpoint_definite_integral_success(client: AsyncClient):
    response = await client.post("/calculus/evaluate", json={
        "expression": "3*x**2",
        "operation": "integrate",
        "integration_bounds": [0, 2] # Integral of 3x^2 is x^3. From 0 to 2, it's 2^3 - 0^3 = 8
    })
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == "8"
    assert data["is_definite_integral"]

# --- Error Cases ---
async def test_calculus_endpoint_invalid_expression_error(client: AsyncClient):
    response = await client.post("/calculus/evaluate", json={
        "expression": "x** / sin(x", # Invalid syntax
        "operation": "differentiate"
    })
    assert response.status_code == 400
    assert "Invalid expression" in response.json()["detail"]

async def test_calculus_endpoint_bounds_with_differentiation_error(client: AsyncClient):
    """ Test that providing bounds for a differentiation operation fails. """
    response = await client.post("/calculus/evaluate", json={
        "expression": "x",
        "operation": "differentiate",
        "integration_bounds": [0, 1]
    })
    # This is caught by our Pydantic model validator
    assert response.status_code == 422
    assert "`integration_bounds` must not be provided" in response.json()["detail"][0]["msg"]
