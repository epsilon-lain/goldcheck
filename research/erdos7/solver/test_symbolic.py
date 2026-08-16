"""Tests for the symbolic exponent-cone machinery in ``symbolic.py``."""

import pytest

from certificate import delta_lower
from covering import factor
from symbolic import (
    Lin,
    all_primes_condition,
    delta_lower_fixed,
    kernel_deficiency_bound,
    lift,
    mine_families,
    power_lift_criterion,
    sigma_fixed,
    surviving_candidates,
)


PRIMES = [11, 13, 17, 19, 23, 29, 31, 37]


def _fixed(primes, exps):
    return delta_lower_fixed(tuple(primes), tuple(exps))


def test_kernel_bound_matches_numeric_squarefree():
    coverage, delta = kernel_deficiency_bound([3, 5, 7])
    assert (coverage.const, coverage.coeff) == (89, 70)
    assert (delta.const, delta.coeff) == (-89, 35)
    for q in PRIMES:
        n = 3 * 5 * 7 * q
        assert delta.eval(q) == delta_lower(n)


def test_power_lift_criterion_task_b():
    _, base = kernel_deficiency_bound([3, 5, 7])
    c = sigma_fixed([5, 7], {5: 1, 7: 1})
    ok, threshold, diff = power_lift_criterion(base, 3, c, 11)
    assert ok and threshold == 11
    assert (diff.const, diff.coeff) == (-226, 22)


def test_power_lift_criterion_task_c():
    _, base = kernel_deficiency_bound([3, 5, 7])
    d2 = lift(base, 3, sigma_fixed([5, 7], {5: 1, 7: 1}))
    assert (d2.const, d2.coeff) == (-315, 57)
    c = sigma_fixed([3, 7], {3: 2, 7: 1})
    ok, threshold, diff = power_lift_criterion(d2, 5, c, 11)
    assert ok and threshold == 11
    assert (diff.const, diff.coeff) == (-1364, 124)


@pytest.mark.parametrize("a", [1, 2, 3, 4, 5, 6])
@pytest.mark.parametrize("q", PRIMES)
def test_family_3_a_5_7_q(a, q):
    # 3^a * 5 * 7 * q is not a covering number for every a >= 1, q >= 11.
    bound = _fixed([3, 5, 7, q], [a, 1, 1, 1])
    assert bound >= 1


@pytest.mark.parametrize("b", [1, 2, 3, 4, 5, 6])
@pytest.mark.parametrize("q", PRIMES)
def test_family_9_5_b_7_q(b, q):
    # 3^2 * 5^b * 7 * q is not a covering number for every b >= 1, q >= 11.
    bound = _fixed([3, 5, 7, q], [2, b, 1, 1])
    assert bound >= 1


def test_delta_lower_fixed_matches_certificate():
    for N in (15, 105, 315, 385, 455, 945, 1155, 1365, 3465, 4095, 5775, 10395, 12285, 17325):
        fs = factor(N)
        primes = tuple(p for p, _ in fs)
        exps = tuple(e for _, e in fs)
        assert delta_lower_fixed(primes, exps) == delta_lower(N)


def test_all_primes_condition():
    assert all_primes_condition([3, 5, 7, 11], {3: 3, 5: 2, 7: 1, 11: 1})
    assert not all_primes_condition([3], {3: 1})  # 3 > tau(1) = 1
    assert not all_primes_condition([3, 5], {3: 1, 5: 1})  # 3 > tau(5)=2
    assert all_primes_condition([3, 5, 7, 11], {3: 3, 5: 1, 7: 1, 11: 1})


def test_scalar_bound_survivor_is_51975():
    # This is the survivor under the *chained scalar* bound only; the full
    # prime-power Lemma 4.10 bound excludes 51975 (see test_full_bound.py).
    survivors = surviving_candidates([3, 5, 7, 11], 5)
    assert survivors
    N, exps = survivors[0]
    assert N == 51975
    assert exps == {3: 3, 5: 2, 7: 1, 11: 1}


def test_miner_finds_key_families():
    result = mine_families([3, 5, 7], max_exponent=3)
    family_keys = {
        (f.free, tuple(sorted(f.exps.items())))
        for f in result.families
    }
    assert (3, ((3, 1), (5, 1), (7, 1))) in family_keys
    assert (5, ((3, 2), (5, 1), (7, 1))) in family_keys


def test_lin_arithmetic():
    a = Lin(3, 5)
    b = Lin(-2, 7)
    assert (a + b) == Lin(1, 12)
    assert (3 * a) == Lin(9, 15)
    assert a.eval(4) == 23
