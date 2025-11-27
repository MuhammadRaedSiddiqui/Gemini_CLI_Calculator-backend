import pytest
import numpy as np
from app.services.matrices import perform_matrix_operation
from app.models.matrices import MatrixOperation

# --- Test Matrix Multiplication ---
def test_matrix_multiply_success():
    m1 = [[1, 2], [3, 4]]
    m2 = [[5, 6], [7, 8]]
    result, shape1, shape2 = perform_matrix_operation(MatrixOperation.multiply, m1, m2)
    assert result == [[19, 22], [43, 50]]
    assert shape1 == "2x2"
    assert shape2 == "2x2"

def test_matrix_multiply_incompatible_shape_error():
    with pytest.raises(ValueError, match="Incompatible shapes for multiplication"):
        perform_matrix_operation(MatrixOperation.multiply, [[1, 2]], [[3], [4], [5]])

# --- Test Determinant ---
def test_determinant_success():
    # Determinant of [[1, 2], [3, 4]] is 1*4 - 2*3 = -2
    result, _, _ = perform_matrix_operation(MatrixOperation.determinant, [[1, 2], [3, 4]])
    assert pytest.approx(result) == -2.0

def test_determinant_not_square_error():
    with pytest.raises(ValueError, match="Matrix must be square to calculate its determinant"):
        perform_matrix_operation(MatrixOperation.determinant, [[1, 2, 3], [4, 5, 6]])

# --- Test Inverse ---
def test_inverse_success():
    m = [[1, 2], [3, 4]]
    result, _, _ = perform_matrix_operation(MatrixOperation.inverse, m)
    expected_inverse = [[-2.0, 1.0], [1.5, -0.5]]
    assert np.allclose(result, expected_inverse)

def test_inverse_of_singular_matrix_error():
    # This matrix is singular (determinant is 0), so it cannot be inverted.
    with pytest.raises(ValueError, match="Matrix is singular and cannot be inverted"):
        perform_matrix_operation(MatrixOperation.inverse, [[1, 1], [1, 1]])

def test_inverse_not_square_error():
    with pytest.raises(ValueError, match="Matrix must be square to be inverted"):
        perform_matrix_operation(MatrixOperation.inverse, [[1, 2, 3], [4, 5, 6]])
