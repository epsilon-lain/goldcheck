# M14 generalization: exact 3-adic fibre budget and the `a=4` affine barrier

This note extracts the part of M14 that generalizes for free in the 3-adic
exponent and records an exact method-level obstruction at the next same-support
frontier.

Let

`N = 3^a M`,  `gcd(3,M)=1`,

and saturate a hypothetical distinct divisor-modulus cover by adding arbitrary
classes at missing divisor moduli.

## 1. Parameterized 3-adic fibre budget

The pure moduli `3,9,...,3^a` cover at most

`3^(a-1)+...+1 = (3^a-1)/2`

residues modulo `3^a`.  Therefore at least

`s_a = (3^a+1)/2`

3-adic fibres survive.

Fix `m|M`, `m>1`, and select any `s_a` surviving fibres.  The mixed moduli

`m,3m,...,3^a m`

induce at most

`k_m(r) <= 1 + sum_{j=1}^a 1[r == c_{j,m} (mod 3^j)]`

classes modulo `m` in fibre `r`.  For fixed `j`, at most `3^(a-j)` selected
fibres can satisfy one prescribed residue modulo `3^j`, hence

`sum_r k_m(r) <= s_a + sum_{j=1}^a 3^(a-j) = 3^a`.

Pointwise, `1 <= k_m(r) <= a+1`.  After grouping exact `M`-moduli by
square-free support,

`b_S = sum_{sqf(m)=S} 1/m`,

we obtain the exact support-charge constraints

`b_S <= q_S(r) <= (a+1)b_S`,

`sum_{r=1}^{s_a} q_S(r) <= 3^a b_S`.

For `a=3` this is exactly the M14 triple `(14,4,27)`.

## 2. The next same-support frontier

The next survivor with the same five-prime `M` support is

`34459425 = 3^4 * 5^2 * 7 * 11 * 13 * 17`.

Now

`s_4=41`, pointwise multiplier `5`, cross-fibre budget `81`.

So an M14-style affine support proof would need nonnegative weights `lambda_S`
and a constant `C` such that on the whole box `[b_S,5b_S]`

`rho(q) >= C - sum_S lambda_S q_S`

and simultaneously

`41 C - 81 sum_S lambda_S b_S > 0`.

Keeping the old M14 weights already fails: the exact box minimum is

`C_5 = 273899/425425`,

and the resulting margin is

`41*C_5 - 81*(144411/425425) = -3928/3575 < 0`.

## 3. Stronger result: exact no-go for the entire nonnegative affine class

The failure is not an artifact of the old weights.

`solver/m14_generalization.py` contains a 32-corner exact dual certificate.
There are nonnegative rational coefficients `alpha_i`, all with denominator
`227239`, such that

`sum_i alpha_i = 41`,

and for every one of the 31 support coordinates,

`sum_i alpha_i q_S^(i) = 81 b_S`.

The same exact combination of the independence-polynomial values is

`sum_i alpha_i rho(q^(i)) = -316412/425425 < 0`.

Therefore any affine inequality valid on the whole box,

`C <= rho(q) + sum_S lambda_S q_S`,  `lambda_S >= 0`,

satisfies, after multiplying those 32 corner inequalities by `alpha_i` and
summing,

`41 C - 81 sum_S lambda_S b_S <= -316412/425425 < 0`.

Hence:

> **No certificate in the M14 nonnegative affine support-box class can exclude
> the `a=4` frontier using only the coarse `(41 fibres, 81 budget, factor-5
> box)` information.**

This is a method-level obstruction, not a covering construction and not a
no-go for Clique-Shearer itself.  It says the next successful proof must retain
more structure than the coarse per-support box and first-moment cross-fibre
budget — for example actual 3-adic compatibility, higher cross-fibre moments,
or a nonlinear/transport certificate.

The dual obstruction is checked using exact `Fraction` arithmetic; no floating
optimizer is trusted by the verifier.
