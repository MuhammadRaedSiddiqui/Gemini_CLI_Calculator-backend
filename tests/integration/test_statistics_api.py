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
async def test_stats_endpoint_mean_success(client: AsyncClient):
    response = await client.post("/statistics/evaluate", json={
        "operation": "mean",
        "data": [10, 20, 30]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 20.0
    assert data["operation"] == "mean"
    assert data["dataset_size"] == 3

async def test_stats_endpoint_std_dev_success(client: AsyncClient):
    response = await client.post("/statistics/evaluate", json={
        "operation": "std_dev",
        "data": [1, 2, 3, 4, 5]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == pytest.approx(1.41421356)

async def test_stats_endpoint_variance_success(client: AsyncClient):
    response = await client.post("/statistics/evaluate", json={
        "operation": "variance",
        "data": [1, 2, 3, 4, 5]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 2.0


# --- Error Cases ---
async def test_stats_endpoint_empty_data_error(client: AsyncClient):
    """ Test API response for an empty data list. """
    response = await client.post("/statistics/evaluate", json={
        "operation": "mean",
        "data": []
    })
    # Pydantic's `conlist(min_length=1)` catches this.
    assert response.status_code == 422
    assert "List should have at least 1 item" in response.json()["detail"][0]["msg"]
