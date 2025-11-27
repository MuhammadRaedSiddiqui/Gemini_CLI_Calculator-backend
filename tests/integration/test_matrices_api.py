import pytest
from httpx import AsyncClient, ASGITransport
import numpy as np
from app.main import app

pytestmark = pytest.mark.asyncio

@pytest.fixture
async def client():
    """ Create an async test client for the app. """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

# --- Success Cases ---
async def test_matrices_endpoint_multiply_success(client: AsyncClient):
    response = await client.post("/matrices/evaluate", json={
        "operation": "multiply",
        "matrix1": [[1, 2], [3, 4]],
        "matrix2": [[5, 6], [7, 8]]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == [[19, 22], [43, 50]]
    assert data["operation"] == "multiply"

async def test_matrices_endpoint_determinant_success(client: AsyncClient):
    response = await client.post("/matrices/evaluate", json={
        "operation": "determinant",
        "matrix1": [[1, 2], [3, 4]]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == pytest.approx(-2.0)

async def test_matrices_endpoint_inverse_success(client: AsyncClient):
    response = await client.post("/matrices/evaluate", json={
        "operation": "inverse",
        "matrix1": [[1, 2], [3, 4]]
    })
    assert response.status_code == 200
    data = response.json()
    assert np.allclose(data["result"], [[-2.0, 1.0], [1.5, -0.5]])

# --- Error Cases ---
async def test_matrices_endpoint_missing_matrix2_for_multiply_error(client: AsyncClient):
    response = await client.post("/matrices/evaluate", json={
        "operation": "multiply",
        "matrix1": [[1, 2]]
        # Missing matrix2
    })
    assert response.status_code == 422 # Pydantic validation error
    assert "`matrix2` is required for multiplication" in response.json()["detail"][0]["msg"]

async def test_matrices_endpoint_incompatible_shapes_error(client: AsyncClient):
    response = await client.post("/matrices/evaluate", json={
        "operation": "multiply",
        "matrix1": [[1, 2]], # Shape (1, 2)
        "matrix2": [[1, 2], [3, 4], [5, 6]] # Shape (3, 2)
    })
    assert response.status_code == 400
    assert "Incompatible shapes for multiplication" in response.json()["detail"]

async def test_matrices_endpoint_singular_matrix_inverse_error(client: AsyncClient):
    response = await client.post("/matrices/evaluate", json={
        "operation": "inverse",
        "matrix1": [[1, 1], [1, 1]]
    })
    assert response.status_code == 400
    assert "Matrix is singular and cannot be inverted" in response.json()["detail"]
