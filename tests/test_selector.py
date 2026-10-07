import numpy as np
import pytest

from pm_bg_aes.selector import SUPPORTED_SIZES, select_matrix_size, select_matrix_size_for


@pytest.mark.parametrize("size,entropy,expected", [
    (0, 0.0, 4), (49999, 4.999, 4), (49999, 5.0, 6), (49999, 7.9, 6),
    (50000, 5.999, 8), (50000, 6.0, 12), (499999, 0.0, 8), (499999, 6.0, 12),
    (500000, 6.999, 16), (500000, 7.0, 24), (4999999, 0.0, 16),
    (4999999, 7.0, 24), (5000000, 7.499, 32), (5000000, 7.5, 48),
    (20000000, 0.0, 32), (20000000, 8.0, 48),
])
def test_selector_boundaries(size, entropy, expected):
    assert select_matrix_size_for(size, entropy) == expected


def test_selector_matches_notebook_on_real_inputs():
    rng = np.random.RandomState(0)
    assert select_matrix_size(np.zeros(6000, dtype=np.uint8)) == 4
    assert select_matrix_size(rng.randint(0, 256, 100000).astype(np.uint8)) == 12
    assert select_matrix_size(np.zeros(600000, dtype=np.uint8)) == 16


def test_supported_sizes_complete():
    assert SUPPORTED_SIZES == (4, 6, 8, 12, 16, 24, 32, 48)
