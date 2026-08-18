from fractions import Fraction

from m35_quantitative_lifting import (
    EXPECTED_LIFT_GAPS,
    M16_EXPECTED_MARGINS,
    M25_P19_MARGIN,
    UNRESOLVED_CANONICAL,
    lift_gap,
    lifted_seed_audit,
    m16_tuple_certificate,
    m25_p19_certificate,
)


def test_m16_extended_margins_are_exact_and_positive():
    for primes, expected in M16_EXPECTED_MARGINS.items():
        cert = m16_tuple_certificate(primes)
        assert cert["summed_rho_margin"] == expected > 0
        assert cert["proper_non5_min"] > 0
        assert cert["completion_upper_max"] < 0


def test_m25_p19_quantitative_margin():
    cert = m25_p19_certificate()
    assert cert["summed_rho_margin"] == M25_P19_MARGIN > 0
    assert cert["proper_non5_min"] > 0
    assert cert["completion_upper_max"] < 0


def test_all_five_lift_gaps_are_exactly_positive():
    margins = {(7, 11, 13, 19): M25_P19_MARGIN, **M16_EXPECTED_MARGINS}
    for primes, margin in margins.items():
        assert lift_gap(primes, margin) == EXPECTED_LIFT_GAPS[primes] > 0


def test_m35_seed_reduction():
    out = lifted_seed_audit()
    assert out["verified"]
    assert out["lifted_seed_count"] == 5
    assert len(out["lifted_numbers"]) == 5
    assert out["unresolved_canonical"] == UNRESOLVED_CANONICAL
    assert UNRESOLVED_CANONICAL == 3**5 * 5**2 * 7 * 11 * 13 * 17
