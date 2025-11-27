import pytest
from httpx import AsyncClient, ASGITransport
# We need to import our app object from our app
from app.main import app

# Mark all tests in this file as asyncio
pytestmark = pytest.mark.asyncio

@pytest.fixture
async def client():
    """
    Create an async test client for the app.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

async def test_evaluate_endpoint_success(client: AsyncClient):
    """
    Test successful evaluation of a valid expression.
    """
    response = await client.post("/arithmetic/evaluate", json={"expression": "2 * (3 + 5)"})
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 16.0
    assert data["expression"] == "2 * (3 + 5)"

async def test_evaluate_endpoint_invalid_expression(client: AsyncClient):
    """
    Test evaluation of an invalid or incomplete expression.
    """
    response = await client.post("/arithmetic/evaluate", json={"expression": "2 * (3 +"})
    assert response.status_code == 400
    assert "Invalid or malformed expression" in response.json()["detail"]

async def test_evaluate_endpoint_division_by_zero(client: AsyncClient):
    """
    Test for division by zero error. Sympy returns zoo, which raises a ValueError on float conversion.
    """
    response = await client.post("/arithmetic/evaluate", json={"expression": "1 / 0"})
    assert response.status_code == 400
    assert "Invalid or malformed expression" in response.json()["detail"]

async def test_evaluate_endpoint_empty_expression(client: AsyncClient):
    """
    Test evaluation of an empty expression string.
    """
    response = await client.post("/arithmetic/evaluate", json={"expression": ""})
    assert response.status_code == 400
    assert "Invalid or malformed expression" in response.json()["detail"]

async def test_health_check(client: AsyncClient):
    """
    Test the health check endpoint to ensure the app is running.
    """
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
