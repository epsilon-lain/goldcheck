from m73_p4222_open3_two_seed_reduction import (
    EXPECTED,EXPONENTS,HARD_SEEDS,goodness_reference,proof_branch,reduction_audit,
)


def test_two_exact_positive_goodness_references():
    for primes,(C,margin,argmin) in EXPECTED.items():
        cert=goodness_reference(primes)
        assert cert["C"]==C
        assert cert["summed_goodness_margin"]==margin>0
        assert cert["argmin_bits"]==argmin


def test_only_two_hard_seed_tuples_remain():
    audit=reduction_audit()
    assert audit["exponent_placement"]==EXPONENTS
    assert audit["hard_seed_count"]==2
    assert audit["hard_seed_prime_tuples"]==HARD_SEEDS
    assert all(proof_branch(s)=="M73-hard-seed" for s in HARD_SEEDS)


def test_tail_branches():
    assert proof_branch((3,5,7,11,13,23))=="M73-goodness-13-23-scale"
    assert proof_branch((3,5,7,11,17,19))=="M73-goodness-17-19-scale"
    assert proof_branch((3,5,7,13,17,19))=="McNew-Setty-off11"
