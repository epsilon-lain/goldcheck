from m43_p62_direct_frontier import (
    P612,
    P62,
    SEEDS,
    direct_reduction_branch,
    frontier_audit,
    placement_scan,
)


def test_m43_placement_scan():
    out = placement_scan()
    assert out["assignment_count"] == 30
    assert set(out["exceptional_placements"]) == {P62, P612}
    assert out["max_directly_killed_R"] < 1


def test_m43_eight_seed_reduction():
    out = frontier_audit()
    assert out["verified"]
    assert out["seed_count"] == 8 == len(SEEDS)
    for primes, exponents in SEEDS:
        assert direct_reduction_branch(primes, exponents) == "seed"
