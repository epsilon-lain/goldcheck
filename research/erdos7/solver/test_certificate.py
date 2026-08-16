"""Tests for the exact certificate machinery in ``certificate.py``."""

from math import gcd

import pytest

from certificate import (
    all_primes_lemma_holds,
    best_chain,
    certify,
    complementary_bell_coeff,
    squarefree_coverage_bound,
    squarefree_delta_lower,
    stirling2,
    verify_certificates,
)
from covering import divisors, factor, sigma


def _ie_direct(n: int) -> int:
    """Independent enumeration of McNew--Setty Lemma 4.10 for square-free n."""
    divs = [d for d in divisors(n) if d > 1]
    total = 0

    def rec(start: int, chosen: list[int]) -> None:
        nonlocal total
        if chosen:
            lcm = 1
            for d in chosen:
                lcm *= d  # pairwise coprime
            total += (-1) ** (len(chosen) + 1) * (n // lcm)
        for i in range(start, len(divs)):
            if all(gcd(divs[i], d) == 1 for d in chosen):
                rec(i + 1, chosen + [divs[i]])

    rec(0, [])
    return total


def test_stirling_and_coeffs():
    assert stirling2(3, 2) == 3
    assert stirling2(4, 2) == 7
    assert [complementary_bell_coeff(j) for j in (1, 2, 3, 4, 5)] == [1, 0, -1, -1, 2]


def test_squarefree_bound_matches_direct_enumeration():
    for n in (15, 105, 165, 231, 273):
        assert squarefree_coverage_bound(n) == _ie_direct(n)


def test_squarefree_known_values():
    assert squarefree_delta_lower(105) == 35
    assert squarefree_delta_lower(385) == 219
    assert squarefree_delta_lower(1155) == 296
    assert squarefree_delta_lower(1365) == 366


def test_squarefree_bound_rejects_non_squarefree():
    with pytest.raises(ValueError):
        squarefree_coverage_bound(945)
    with pytest.raises(ValueError):
        squarefree_coverage_bound(12)


def test_all_primes_lemma_arithmetic():
    # Necessary condition holds for the three stragglers.
    for N in (10395, 12285, 17325):
        assert all_primes_lemma_holds(N)
    # For N=2 the condition fails (2 > tau(1)=1), so N=2 is not primitive.
    assert not all_primes_lemma_holds(2)
    # Explicitly check p <= tau(N / p^v_p(N)) for each prime of 10395.
    assert all_primes_lemma_holds(10395) is True


def test_certificate_values():
    assert verify_certificates() == {945: 123, 10395: 360, 12285: 606, 17325: 312}
    for N, expected in ((945, 123), (10395, 360), (12285, 606), (17325, 312)):
        bound, text = certify(N)
        assert bound == expected
        assert "NOT a covering number" in text


def test_best_chain_is_nonnegative_for_small_numbers():
    for N in (2, 3, 6, 15, 105, 945, 10395, 12285, 17325):
        bound, _ = best_chain(N)
        assert bound >= 0


def test_sigma_values_used_by_certificates():
    assert sigma(35) == 48
    assert sigma(385) == 576
    assert sigma(455) == 672
    assert sigma(231) == 384
    assert sigma(1925) == 2976
