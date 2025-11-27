import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

pytestmark = pytest.mark.asyncio

@pytest.fixture
async def client():
    """ Create an async test client for the app. """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

# --- Success Cases ---
async def test_complex_endpoint_multiplication_success(client: AsyncClient):
    response = await client.post("/complex/evaluate", json={
        "num1": "3+4j",
        "num2": "1-2j",
        "operation": "multiply"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == "11-2j"
    assert data["calculation"] == "(3+4j) * (1-2j)"

async def test_complex_endpoint_division_success(client: AsyncClient):
    response = await client.post("/complex/evaluate", json={
        "num1": "4+2j",
        "num2": "1+1j",
        "operation": "divide"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == "3-1j"

# --- Error Cases ---
async def test_complex_endpoint_division_by_zero_error(client: AsyncClient):
    response = await client.post("/complex/evaluate", json={
        "num1": "5+5j",
        "num2": "0",
        "operation": "divide"
    })
    assert response.status_code == 400
    assert "division by zero is not allowed" in response.json()["detail"]

async def test_complex_endpoint_invalid_number_string_error(client: AsyncClient):
    """ Test with a string that cannot be parsed into a complex number. """
    response = await client.post("/complex/evaluate", json={
        "num1": "5+5i",  # 'i' is not valid, must be 'j'
        "num2": "1+1j",
        "operation": "add"
    })
    # This should be caught by our Pydantic validator.
    assert response.status_code == 422
    assert "not a valid complex number" in response.json()["detail"][0]["msg"]

async def test_complex_endpoint_invalid_operation_error(client: AsyncClient):
    """ Test with an operation that is not in the Enum. """
    response = await client.post("/complex/evaluate", json={
        "num1": "1+1j",
        "num2": "2+2j",
        "operation": "power" # Not a valid operation
    })
    assert response.status_code == 422
    assert "Input should be 'add', 'subtract', 'multiply' or 'divide'" in response.json()["detail"][0]["msg"]
