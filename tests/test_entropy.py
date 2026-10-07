import math

import numpy as np

from pm_bg_aes.entropy import shannon_entropy


def test_entropy_single_byte_is_zero():
    assert shannon_entropy(np.full(100, 7, dtype=np.uint8)) == 0.0


def test_entropy_two_equiprobable_is_one():
    d = np.array([0, 255] * 50, dtype=np.uint8)
    assert shannon_entropy(d) == 1.0


def test_entropy_uniform_is_eight():
    d = np.tile(np.arange(256, dtype=np.uint8), 4)
    assert abs(shannon_entropy(d) - 8.0) < 1e-9


def test_entropy_known_text_value():
    d = np.frombuffer(b"aaaaabbbbb", dtype=np.uint8)
    assert abs(shannon_entropy(d) - 1.0) < 1e-12


def test_entropy_empty_defined_as_zero():
    assert shannon_entropy(np.empty(0, dtype=np.uint8)) == 0.0
