"""Side-effect-free Cayley-Dickson numerical kernel.

Historically, reusable multiplication helpers lived in ``cd_embedding.py``.
Importing that module also executed its full 16D/32D analysis, so every caller
paid the multi-minute analysis cost before its own computation began.  This
module is the import-safe API; ``cd_embedding.py`` remains the executable
analysis document and imports the same functions from here.
"""

from __future__ import annotations

import numpy as np


def cd_conj(x):
    """Conjugate a Cayley-Dickson vector."""

    conjugate = -x.copy()
    conjugate[0] = x[0]
    return conjugate


def cd_multiply(a, b, n):
    """Multiply two vectors in the ``2**n`` dimensional CD algebra."""

    dimension = 2**n
    assert len(a) == dimension and len(b) == dimension
    if n == 0:
        return a * b
    half = dimension // 2
    a1, a2 = a[:half], a[half:]
    b1, b2 = b[:half], b[half:]
    part1 = cd_multiply(a1, b1, n - 1) - cd_multiply(cd_conj(b2), a2, n - 1)
    part2 = cd_multiply(b2, a1, n - 1) + cd_multiply(a2, cd_conj(b1), n - 1)
    return np.concatenate([part1, part2])


def build_mult_table(n):
    """Build the full multiplication table for a ``2**n`` dimensional algebra."""

    dimension = 2**n
    table = np.zeros((dimension, dimension, dimension), dtype=float)
    for i in range(dimension):
        for j in range(dimension):
            ei = np.zeros(dimension)
            ej = np.zeros(dimension)
            ei[i] = 1.0
            ej[j] = 1.0
            table[i, j, :] = cd_multiply(ei, ej, n)
    return table


def left_mult_matrix(a, table):
    """Return ``L_a`` such that ``L_a @ x == a * x``."""

    dimension = len(a)
    matrix = np.zeros((dimension, dimension))
    for j in range(dimension):
        for k in range(dimension):
            if a[k] != 0:
                matrix[:, j] += a[k] * table[k, j]
    return matrix


def right_mult_matrix(b, table):
    """Return ``R_b`` such that ``R_b @ x == x * b``."""

    dimension = len(b)
    matrix = np.zeros((dimension, dimension))
    for j in range(dimension):
        for k in range(dimension):
            if b[k] != 0:
                matrix[:, j] += b[k] * table[j, k]
    return matrix


def null_space(matrix, tolerance=1e-10):
    """Compute a row-basis for the numerical null space of ``matrix``."""

    _u, singular_values, vh = np.linalg.svd(matrix)
    null_dimension = int(np.sum(singular_values < tolerance))
    if null_dimension == 0:
        return np.zeros((0, matrix.shape[1]))
    return vh[-null_dimension:]
