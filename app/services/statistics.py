import numpy as np
from typing import List
from app.models.statistics import StatisticsOperation

def perform_statistics_operation(
    operation: StatisticsOperation,
    data: List[float]
) -> float:
    """
    Performs a statistical calculation on a list of numbers.

    Args:
        operation: The statistical operation to perform.
        data: A list of numbers (dataset).

    Returns:
        The result of the calculation as a float.
        
    Raises:
        ValueError: If an unsupported operation is provided.
    """
    # The Pydantic model ensures data is not empty, but we can double-check.
    if not data:
        raise ValueError("Dataset cannot be empty.")

    dataset = np.array(data)

    if operation == StatisticsOperation.mean:
        result = np.mean(dataset)
    elif operation == StatisticsOperation.median:
        result = np.median(dataset)
    elif operation == StatisticsOperation.std_dev:
        # ddof=0 for population standard deviation, which is numpy's default.
        # For sample standard deviation, use ddof=1.
        result = np.std(dataset)
    elif operation == StatisticsOperation.variance:
        result = np.var(dataset)
    else:
        # Should not be reachable with Enum validation
        raise ValueError(f"Invalid or unsupported statistics operation: {operation}")

    return float(result)
