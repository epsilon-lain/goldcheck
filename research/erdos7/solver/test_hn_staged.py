"""Tests for the Milestone 13 Q2 finite 27-fiber adversary."""

from hn_staged import (
    min_surviving_fibers,
    surviving_fibers,
    verify_pure3_bruteforce,
    worst_total_load,
)


def test_min_survivors_is_14():
    assert min_surviving_fibers() == 14


def test_survivor_set_example():
    # Disjoint pure classes: c1=0 mod3, c2=1 mod9, c3=2 mod27 give 14 survivors.
    S = surviving_fibers(0, 1, 2)
    assert len(S) == 14
    assert all(r % 3 != 0 and r % 9 != 1 and r != 2 for r in S)


def test_bruteforce_verifier():
    res = verify_pure3_bruteforce()
    assert res["min_survivors"] == 14
    assert res["min_is_14"] is True
    assert res["closed_form_matches_bruteforce"] is True


def test_worst_total_load_bound():
    S = {0, 3, 6, 9, 12, 15, 18, 21, 24}
    # best mod3 = 9, best mod9 = 3, best mod27 = 1, plus |S| = 9.
    assert worst_total_load(S) == 9 + 9 + 3 + 1
