import pytest
from app.services.statistics import perform_statistics_operation
from app.models.statistics import StatisticsOperation

@pytest.fixture
def sample_data():
    """A simple dataset for testing."""
    return [1, 2, 3, 4, 5]

def test_mean_calculation(sample_data):
    # Mean of [1, 2, 3, 4, 5] is 15 / 5 = 3
    assert perform_statistics_operation(StatisticsOperation.mean, sample_data) == 3.0

def test_median_calculation(sample_data):
    # Median of [1, 2, 3, 4, 5] is 3
    assert perform_statistics_operation(StatisticsOperation.median, sample_data) == 3.0

def test_median_with_even_dataset():
    assert perform_statistics_operation(StatisticsOperation.median, [1, 2, 3, 4]) == 2.5

def test_std_dev_calculation(sample_data):
    # Population standard deviation of [1, 2, 3, 4, 5] is sqrt(2)
    assert pytest.approx(perform_statistics_operation(StatisticsOperation.std_dev, sample_data)) == 1.41421356

def test_variance_calculation(sample_data):
    # Variance of [1, 2, 3, 4, 5] is 2
    assert perform_statistics_operation(StatisticsOperation.variance, sample_data) == 2.0

def test_empty_dataset_error():
    """
    Test that the service function raises a ValueError for an empty dataset.
    Note: Pydantic's conlist should prevent this from being called via the API.
    """
    with pytest.raises(ValueError, match="Dataset cannot be empty"):
        perform_statistics_operation(StatisticsOperation.mean, [])
