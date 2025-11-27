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
async def test_algebra_endpoint_quadratic_real_roots_success(client: AsyncClient):
    response = await client.post("/algebra/poly-solve", json={
        "coefficients": [1, -3, 2] # x^2 - 3x + 2 = 0
    })
    assert response.status_code == 200
    data = response.json()
    assert len(data["roots"]) == 2
    assert "1.0000" in data["roots"]
    assert "2.0000" in data["roots"]
    assert data["polynomial"] == "x**2 - 3*x + 2"

async def test_algebra_endpoint_quadratic_complex_roots_success(client: AsyncClient):
    response = await client.post("/algebra/poly-solve", json={
        "coefficients": [1, 0, 4] # x^2 + 4 = 0
    })
    assert response.status_code == 200
    data = response.json()
    assert len(data["roots"]) == 2
    assert "0.0000+2.0000j" in data["roots"]
    assert "0.0000-2.0000j" in data["roots"]
    assert data["polynomial"] == "x**2 + 4"

async def test_algebra_endpoint_linear_equation_success(client: AsyncClient):
    response = await client.post("/algebra/poly-solve", json={
        "coefficients": [3, -9] # 3x - 9 = 0
    })
    assert response.status_code == 200
    data = response.json()
    assert len(data["roots"]) == 1
    assert "3.0000" in data["roots"]
    assert data["polynomial"] == "3*x - 9"

# --- Error Cases ---
async def test_algebra_endpoint_insufficient_coeffs_pydantic_error(client: AsyncClient):
    # The `conlist(min_length=1)` in Pydantic model handles the empty list case.
    # However, our service layer requires min_length=2. This tests the service layer error.
    response = await client.post("/algebra/poly-solve", json={
        "coefficients": [5]
    })
    assert response.status_code == 400
    assert "At least two coefficients are required" in response.json()["detail"]

async def test_algebra_endpoint_empty_coeffs_pydantic_error(client: AsyncClient):
    # Pydantic's `conlist(min_length=1)` catches this before it hits the service layer.
    response = await client.post("/algebra/poly-solve", json={
        "coefficients": []
    })
    assert response.status_code == 422 # Unprocessable Entity
    assert "List should have at least 1 item" in response.json()["detail"][0]["msg"]
