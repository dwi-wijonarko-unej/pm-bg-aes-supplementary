import numpy as np
import pytest

from pm_bg_aes.permutation import key_matrix, permutation_order, split_n


@pytest.mark.parametrize("n", [4, 6, 8, 12, 16, 24, 32, 48])
def test_permutation_is_orthogonal(n):
    P, Pt = key_matrix(n, for_decrypt=True)
    assert P.shape == (n, n)
    assert np.array_equal(P @ P.T, np.eye(n, dtype=np.int32))
    assert np.array_equal(Pt, P.T)
    assert np.all(P.sum(axis=0) == 1) and np.all(P.sum(axis=1) == 1)


def test_expected_fixed_swaps():
    assert permutation_order(4) == [0, 1, 3, 2]          # p=2,q=2: swap(2,3)
    assert permutation_order(6) == [0, 1, 2, 4, 3, 5]    # p=3,q=3: swap(3,4) only
    p24 = permutation_order(24)
    assert p24[12:16] == [13, 12, 15, 14]               # both swaps for q=12
    assert p24[:12] == list(range(12)) and p24[16:] == list(range(16, 24))


def test_split_n():
    assert split_n(24) == (12, 12)
    assert split_n(6) == (3, 3)
