"""Regression tests for the M14 3-adic generalization and a=4 affine dual."""

from fractions import Fraction

from m14_generalization import a4_generalization_audit, three_adic_budget


def test_three_adic_budget_special_cases():
    assert three_adic_budget(3) == {
        "a": 3,
        "power": 27,
        "surviving_fibres": 14,
        "cross_fibre_budget": 27,
        "pointwise_multiplier": 4,
    }
    assert three_adic_budget(4) == {
        "a": 4,
        "power": 81,
        "surviving_fibres": 41,
        "cross_fibre_budget": 81,
        "pointwise_multiplier": 5,
    }


def test_a4_affine_dual_certificate_is_exact():
    result = a4_generalization_audit()
    assert result["old_lambda_box_min"] == Fraction(273899, 425425)
    assert result["old_lambda_margin"] == Fraction(-3928, 3575)
    assert result["dual_corner_count"] == 32
    assert result["dual_weight_sum"] == 41
    assert result["all_support_budgets_exact"] is True
    assert result["weighted_rho"] == Fraction(-316412, 425425)
    assert result["positive_affine_margin_impossible"] is True
