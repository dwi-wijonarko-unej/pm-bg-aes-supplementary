import numpy as np

from pm_bg_aes import cli
from pm_bg_aes.analysis import (
    adjacent_correlation,
    byte_divergence_same_length,
    byte_histogram,
    chi_square_uniform,
)


def test_histogram_counts():
    h = byte_histogram(np.array([0, 0, 255], dtype=np.uint8))
    assert h.sum() == 3 and h[0] == 2 and h[255] == 1 and len(h) == 256


def test_correlation_nan_on_constant():
    import math

    assert math.isnan(adjacent_correlation(np.full(50, 9, dtype=np.uint8)))
    assert math.isnan(adjacent_correlation(np.empty(0, dtype=np.uint8)))


def test_correlation_perfect_ramp():
    r = adjacent_correlation(np.arange(100, dtype=np.uint8))
    assert abs(r - 1.0) < 1e-9


def test_chi_square_uniform_input():
    out = chi_square_uniform(np.tile(np.arange(256, dtype=np.uint8), 10))
    assert out["statistic"] == 0.0 and out["dof"] == 255


def test_chi_square_pvalue_type():
    out = chi_square_uniform(np.zeros(1000, dtype=np.uint8))
    assert out["statistic"] > 0
    assert out["p_value"] is None or 0.0 <= out["p_value"] <= 1.0


def test_divergence_requires_equal_length():
    import pytest

    with pytest.raises(ValueError):
        byte_divergence_same_length(b"abc", b"abcd")
    assert byte_divergence_same_length(b"abc", b"abc")["divergence"] == 0.0


def test_cli_help_and_verify(tmp_path, capsys):
    import pytest

    with pytest.raises(SystemExit) as e:
        cli.main(["--help"])
    assert e.value.code == 0
    a = tmp_path / "a.bin"
    b = tmp_path / "b.bin"
    a.write_bytes(b"xyz")
    b.write_bytes(b"xyz")
    assert cli.main(["verify", str(a), str(b)]) == 0
    b.write_bytes(b"xy!")
    assert cli.main(["verify", str(a), str(b)]) == 2
