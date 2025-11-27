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
async def test_numbers_endpoint_dec_to_hex_success(client: AsyncClient):
    response = await client.post("/numbers/convert", json={
        "value": "255",
        "from_base": 10,
        "to_base": 16
    })
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == "FF"
    assert data["original_value"] == "255"
    assert data["from_base"] == 10
    assert data["to_base"] == 16

async def test_numbers_endpoint_bin_to_dec_success(client: AsyncClient):
    response = await client.post("/numbers/convert", json={
        "value": "1010",
        "from_base": 2,
        "to_base": 10
    })
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == "10"

async def test_numbers_endpoint_hex_to_octal_success(client: AsyncClient):
    response = await client.post("/numbers/convert", json={
        "value": "C7",
        "from_base": 16,
        "to_base": 8
    })
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == "307"

# --- Error Cases ---
async def test_numbers_endpoint_invalid_value_for_base_error(client: AsyncClient):
    """ '9B' is not a valid number in base 8 (octal). """
    response = await client.post("/numbers/convert", json={
        "value": "9B",
        "from_base": 8,
        "to_base": 10
    })
    assert response.status_code == 400
    assert "Invalid number '9B' for base 8" in response.json()["detail"]

async def test_numbers_endpoint_invalid_from_base_error(client: AsyncClient):
    """ '99' is not a valid base. """
    response = await client.post("/numbers/convert", json={
        "value": "10",
        "from_base": 99,
        "to_base": 10
    })
    assert response.status_code == 422 # Pydantic validation error for Enum
    assert "Input should be 2, 8, 10 or 16" in response.json()["detail"][0]["msg"]
