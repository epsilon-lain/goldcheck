"""Brute-force checks of the conditioned top-layer profile inequality."""

import pytest

from covering import divisors, sigma
from profile import (
    lower_choices,
    max_top_coverage,
    mu,
    profile_capacity,
    top_lifts_met,
    uncovered,
)


def _cases():
    # (N, p, a, M)
    return [
        (27, 3, 3, 1),
        (45, 3, 2, 5),
        (75, 5, 2, 3),
        (81, 3, 4, 1),
    ]


@pytest.mark.parametrize("N,p,a,M", _cases())
def test_top_class_meets_at_most_profile_of_one_fiber(N, p, a, M):
    L = N // p
    for lower in lower_choices(L):
        U = uncovered(N, p, lower)
        for e in [d for d in divisors(M) if d >= 1]:
            d = p ** (a - 1) * e
            bound = mu(U, d)
            top_mod = p**a * e
            for r in range(top_mod):
                met = top_lifts_met(N, p, a, e, r, U)
                assert met <= bound


@pytest.mark.parametrize("N,p,a,M", _cases())
def test_profile_capacity_refines_raw_sigma(N, p, a, M):
    L = N // p
    for lower in lower_choices(L):
        U = uncovered(N, p, lower)
        cap = profile_capacity(p, a, M, U)
        # The raw recurrence charges sigma(M); the profile is never larger.
        assert cap <= sigma(M)


@pytest.mark.parametrize("N,p,a,M", _cases())
def test_profile_capacity_bounds_exact_top_coverage(N, p, a, M):
    L = N // p
    for lower in lower_choices(L):
        U = uncovered(N, p, lower)
        cap = profile_capacity(p, a, M, U)
        assert max_top_coverage(N, p, a, M, U) <= cap


def test_profile_capacity_can_be_strictly_below_sigma():
    # For N=45=3^2*5 the conditioned profile is sometimes strictly below the
    # raw sigma(M)=6 charge, showing the refinement is real.
    N, p, a, M = 45, 3, 2, 5
    capacities = []
    for lower in lower_choices(N // p):
        U = uncovered(N, p, lower)
        capacities.append(profile_capacity(p, a, M, U))
    assert min(capacities) < sigma(M)
