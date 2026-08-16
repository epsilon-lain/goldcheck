"""Independent HiGHS MILP cross-checks of small covering instances."""

from milp import max_coverage_milp


def test_milp_small_exact_values():
    # 15 is square-free odd; max coverage is 8, deficiency 7.
    covered, delta = max_coverage_milp(15)
    assert (covered, delta) == (8, 7)


def test_milp_105_matches_squarefree_bound():
    # 105 is square-free odd; the CRT/Hall bound is tight here (r=70, delta=35).
    covered, delta = max_coverage_milp(105)
    assert (covered, delta) == (70, 35)
