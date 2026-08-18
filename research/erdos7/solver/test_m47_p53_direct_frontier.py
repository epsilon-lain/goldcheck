from m47_p53_direct_frontier import (
    P35,
    P513,
    P53,
    SEEDS,
    direct_reduction_branch,
    frontier_audit,
    placement_scan,
)


def test_m47_three_surviving_placements():
    out = placement_scan()
    assert out["verified"]
    assert out["assignment_count"] == 30
    assert set(out["surviving_placements"]) == {P35, P513, P53}
    assert out["max_directly_killed_R"] < 1


def test_m47_sixteen_seed_reduction():
    out = frontier_audit()
    assert out["verified"]
    assert out["seed_count"] == 16 == len(SEEDS)
    assert out["seed_counts_by_placement"] == {P35: 3, P513: 1, P53: 12}
    for primes, exponents in SEEDS:
        assert direct_reduction_branch(primes, exponents) == "seed"
