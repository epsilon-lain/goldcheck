"""M49: close profile (5,3,1,1,1,1) and recompute the minimal frontier.

M47 reduces P53 to sixteen explicit seeds in three exponent placements.  M48's
three infinite special-coordinate certificates match those placements exactly:

- P35=(3,5,1,1,1,1): use a=3 with distinguished prime 5 at its limit 1/4;
- P513=(5,1,3,1,1,1): use a=5 with distinguished prime 7 at its limit 1/6;
- P53=(5,3,1,1,1,1): use a=5 with distinguished prime 5 at its limit 1/4.

The reference simple-prime baselines dominate every M47 seed in the relevant
placement, so the limit certificates exclude all sixteen seeds.  M47's direct
reduction then closes the whole profile.
"""
from __future__ import annotations

from m26_minimal_frontier import family_number, sorted_profile
from m42_p322_profile_closure import P332, P3222, P422
from m46_frontier_after_ray import profile_closed_after_m45
from m47_p53_direct_frontier import P35, P513, P53, SEEDS
from m48_special_coordinate_limits import (
    a3_five_limit_certificate,
    a5_five_limit_certificate,
    a5_seven_limit_certificate,
)

P63 = (6, 3, 1, 1, 1, 1)
P54 = (5, 4, 1, 1, 1, 1)
MINIMAL_FRONTIER = (P63, P54, P422, P332, P3222)


def p53_seed_closure_audit() -> dict:
    cert_a3_5 = a3_five_limit_certificate()
    cert_a5_5 = a5_five_limit_certificate()
    cert_a5_7 = a5_seven_limit_certificate()
    assert cert_a3_5["summed_rho_margin"] > 0
    assert cert_a5_5["summed_goodness_margin"] > 0
    assert cert_a5_7["summed_goodness_margin"] > 0

    counts = {P35: 0, P513: 0, P53: 0}
    numbers = []
    for primes, exponents in SEEDS:
        exp = tuple(exponents)
        if exp == P35:
            # Stage on 3^3, special finite 5^5 <= x_5(infinity)=1/4.
            # Non-special simples are coordinatewise >= (7,11,13,17).
            assert all(p >= r for p, r in zip(primes[2:], (7, 11, 13, 17)))
            branch = "M48-a3-five-limit"
        elif exp == P513:
            # Unique seed: stage on 3^5, distinguish 7^3 <= x_7(infinity)=1/6.
            J = (primes[1], primes[3], primes[4], primes[5])
            assert all(p >= r for p, r in zip(J, (5, 11, 13, 17)))
            branch = "M48-a5-seven-limit"
        elif exp == P53:
            # Stage on 3^5, distinguish 5^3 <= x_5(infinity)=1/4.
            assert all(p >= r for p, r in zip(primes[2:], (7, 11, 13, 17)))
            branch = "M48-a5-five-limit"
        else:
            raise AssertionError("unexpected M47 seed placement")
        counts[exp] += 1
        numbers.append((family_number(primes, exponents), branch))

    assert counts == {P35: 3, P513: 1, P53: 12}
    assert len(numbers) == 16
    return {
        "seed_count": len(numbers),
        "counts_by_placement": counts,
        "certified_seed_branches": tuple(numbers),
        "all_m47_seeds_excluded": True,
    }


def profile_closed_after_m49(profile) -> bool:
    p = sorted_profile(profile)
    if profile_closed_after_m45(p):
        return True
    return all(a <= b for a, b in zip(p, P53))


def minimal_frontier_dominator(profile):
    p = sorted_profile(profile)
    if profile_closed_after_m49(p):
        return None

    assert p[1] >= 2
    if p[2] == 1:
        # a2=2 is completely closed by M45, so a2>=3.
        assert p[1] >= 3
        if p[1] >= 4:
            # If a1<=4 this lies under the closed P44 profile.
            assert p[0] >= 5
            out = P54
        else:
            assert p[1] == 3
            # Failure of newly closed P53 forces a1>=6.
            assert p[0] >= 6
            out = P63
    else:
        assert p[2] >= 2 and p[0] >= 3
        if p[3] >= 2:
            out = P3222
        elif p[1] >= 3:
            out = P332
        else:
            assert p[1] == 2 and p[2] == 2 and p[0] >= 4
            out = P422

    assert all(a <= b for a, b in zip(out, p))
    return out


def frontier_audit() -> dict:
    closure = p53_seed_closure_audit()
    assert closure["all_m47_seeds_excluded"]
    assert all(not profile_closed_after_m49(p) for p in MINIMAL_FRONTIER)
    for p in MINIMAL_FRONTIER:
        for q in MINIMAL_FRONTIER:
            if p != q:
                assert not all(a <= b for a, b in zip(p, q))

    assert minimal_frontier_dominator(P63) == P63
    assert minimal_frontier_dominator(P54) == P54
    assert minimal_frontier_dominator(P422) == P422
    assert minimal_frontier_dominator(P332) == P332
    assert minimal_frontier_dominator(P3222) == P3222

    assert profile_closed_after_m49(P53)
    assert minimal_frontier_dominator((10, 3, 1, 1, 1, 1)) == P63
    assert minimal_frontier_dominator((8, 6, 1, 1, 1, 1)) == P54
    assert minimal_frontier_dominator((7, 2, 2, 1, 1, 1)) == P422
    assert minimal_frontier_dominator((5, 4, 2, 1, 1, 1)) == P332
    assert minimal_frontier_dominator((4, 3, 2, 2, 1, 1)) == P3222

    return {
        "p53_closure": closure,
        "minimal_frontier": MINIMAL_FRONTIER,
        "frontier_size": len(MINIMAL_FRONTIER),
        "verified": True,
    }


__all__ = [
    "MINIMAL_FRONTIER",
    "P54",
    "P63",
    "frontier_audit",
    "minimal_frontier_dominator",
    "p53_seed_closure_audit",
    "profile_closed_after_m49",
]
