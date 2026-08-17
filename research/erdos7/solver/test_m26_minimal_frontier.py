"""Regression tests for M26 minimal exponent-frontier census."""
from fractions import Fraction
from m26_minimal_frontier import (
    MINIMAL_FRONTIER,
    SEEDS,
    direct_reduction_branch,
    frontier_census,
    minimal_frontier_dominator,
    placement_scan,
    profile_closed_before_m26,
)


def test_m26_exact_minimal_antichain():
    assert MINIMAL_FRONTIER==(
        (5,2,1,1,1,1),
        (4,4,1,1,1,1),
        (3,2,2,1,1,1),
    )
    assert profile_closed_before_m26((4,3,1,1,1,1)) is True
    assert profile_closed_before_m26((2,2,2,2,2,2)) is True
    assert profile_closed_before_m26((20,1,1,1,1,1)) is True
    assert minimal_frontier_dominator((9,2,1,1,1,1))==(5,2,1,1,1,1)
    assert minimal_frontier_dominator((4,4,3,1,1,1))==(4,4,1,1,1,1)
    assert minimal_frontier_dominator((3,2,7,1,1,1))==(5,2,1,1,1,1)
    assert minimal_frontier_dominator((3,3,2,1,1,1))==(3,2,2,1,1,1)


def test_m26_placement_exception_counts():
    s52=placement_scan((5,2,1,1,1,1))
    s44=placement_scan((4,4,1,1,1,1))
    s322=placement_scan((3,2,2,1,1,1))
    assert (s52["assignment_count"],len(s52["exceptional_placements"]))==(30,2)
    assert (s44["assignment_count"],len(s44["exceptional_placements"]))==(15,2)
    assert (s322["assignment_count"],len(s322["exceptional_placements"]))==(60,4)
    assert s52["max_directly_killed_R"]==Fraction(2655728,2675673)<1
    assert s44["max_directly_killed_R"]==Fraction(1815414127,1834619787)<1
    assert s322["max_directly_killed_R"]==Fraction(1300549,1310309)<1


def test_m26_seed_counts_and_seed_branches():
    assert {p:len(SEEDS[p]) for p in MINIMAL_FRONTIER}=={
        (5,2,1,1,1,1):7,
        (4,4,1,1,1,1):11,
        (3,2,2,1,1,1):12,
    }
    for profile in MINIMAL_FRONTIER:
        for primes,exponents in SEEDS[profile]:
            assert direct_reduction_branch(primes,exponents)=="seed"


def test_m26_representative_anchor_kills():
    assert direct_reduction_branch((3,5,7,11,13,37),(5,2,1,1,1,1))=="McNew-Setty-anchor"
    assert direct_reduction_branch((3,5,7,11,13,47),(4,4,1,1,1,1))=="McNew-Setty-anchor"
    assert direct_reduction_branch((3,5,7,11,13,23),(3,2,1,2,1,1))=="McNew-Setty-anchor"


def test_m26_full_census():
    result=frontier_census()
    assert result["minimal_frontier"]==MINIMAL_FRONTIER
    assert result["total_direct_bound_seeds"]==30
    assert result["verified"] is True
