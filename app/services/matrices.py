import numpy as np
from typing import List, Optional, Union, Tuple
from app.models.matrices import MatrixOperation

def perform_matrix_operation(
    operation: MatrixOperation,
    matrix1: List[List[float]],
    matrix2: Optional[List[List[float]]] = None
) -> Tuple[Union[List[List[float]], float], str, Optional[str]]:
    """
    Performs a specified matrix operation using numpy.

    Args:
        operation: The matrix operation to perform.
        matrix1: The first matrix as a list of lists.
        matrix2: The second matrix (required for multiplication).

    Returns:
        A tuple containing:
        - The result (a matrix or a scalar).
        - The shape of matrix1.
        - The shape of matrix2 (if it exists).

    Raises:
        ValueError: For shape mismatches, non-invertible matrices, or other errors.
    """
    try:
        m1 = np.array(matrix1)
        shape1_str = f"{m1.shape[0]}x{m1.shape[1]}"
        shape2_str = None
    except Exception:
        raise ValueError("Invalid format for `matrix1`.")

    if operation == MatrixOperation.determinant:
        if m1.shape[0] != m1.shape[1]:
            raise ValueError("Matrix must be square to calculate its determinant.")
        result = np.linalg.det(m1)
        return float(result), shape1_str, None

    elif operation == MatrixOperation.inverse:
        if m1.shape[0] != m1.shape[1]:
            raise ValueError("Matrix must be square to be inverted.")
        try:
            inverted_matrix = np.linalg.inv(m1)
            return inverted_matrix.tolist(), shape1_str, None
        except np.linalg.LinAlgError:
            # This error is raised for singular matrices
            raise ValueError("Matrix is singular and cannot be inverted.")

    elif operation == MatrixOperation.multiply:
        if matrix2 is None:
            # This should be caught by the Pydantic model, but serves as a safeguard.
            raise ValueError("Matrix multiplication requires a second matrix (`matrix2`).")
        try:
            m2 = np.array(matrix2)
            shape2_str = f"{m2.shape[0]}x{m2.shape[1]}"
        except Exception:
            raise ValueError("Invalid format for `matrix2`.")

        if m1.shape[1] != m2.shape[0]:
            raise ValueError(
                f"Incompatible shapes for multiplication: `matrix1` has shape {shape1_str} "
                f"and `matrix2` has shape {shape2_str}. The number of columns in matrix1 "
                "must equal the number of rows in matrix2."
            )
        
        result_matrix = np.matmul(m1, m2)
        return result_matrix.tolist(), shape1_str, shape2_str
        
    else:
        # Should not be reachable with Enum validation
        raise ValueError(f"Invalid or unsupported matrix operation: {operation}")
