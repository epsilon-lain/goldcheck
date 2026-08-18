from m26_minimal_frontier import P322, SEEDS
from m40_p322_profile_closure import EXPECTED, profile_audit, seed_certificate


def test_m40_exact_seed_certificates():
    assert len(SEEDS[P322]) == 12
    assert set(SEEDS[P322]) == set(EXPECTED)
    for primes, exponents in SEEDS[P322]:
        out = seed_certificate(primes, exponents)
        assert out["summed_rho_margin"] > 0
        assert out["proper_non5_min"] > 0
        assert out["full_non5_min"] > 0
        assert out["noncovering_certified"]


def test_m40_profile_closure():
    out = profile_audit()
    assert out["profile"] == P322
    assert out["seed_count"] == 12
    assert out["all_m26_seeds_excluded"]
    assert out["all_odd_six_prime_numbers_with_profile_noncovering"]
    assert out["minimum_margin"] > 0
