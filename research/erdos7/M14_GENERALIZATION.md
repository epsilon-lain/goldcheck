# M14 generalization: exact 3-adic fibre budget for `3^a M`

This note extracts the part of the M14 proof that generalizes for free in the
3-adic exponent.  It is independent of the particular affine weights used for
`a=3`.

Let

`N = 3^a M`,  `gcd(3,M)=1`,

and saturate a hypothetical distinct divisor-modulus covering by adding an
arbitrary class for every missing divisor.  Work modulo `3^a` first.

## 1. Number of surviving pure-3 fibres

The pure moduli `3,9,...,3^a` cover at most

`3^(a-1) + 3^(a-2) + ... + 1 = (3^a-1)/2`

residues modulo `3^a`.  Therefore at least

`s_a = (3^a+1)/2`

3-adic fibres survive.

For `a=3`, this is `s_3=14`, recovering M14.  For `a=4`, it is `s_4=41`.

## 2. Exact cross-fibre charge budget

Fix `m|M`, `m>1`, and select any `s_a` distinct surviving fibres.  The mixed
moduli

`m, 3m, 9m, ..., 3^a m`

induce at most

`k_m(r) <= 1 + sum_{j=1}^a 1[r == c_{j,m} (mod 3^j)]`

classes modulo `m` inside fibre `r`.

For fixed `j`, among distinct residues modulo `3^a`, at most `3^(a-j)` of the
selected fibres can satisfy one prescribed congruence modulo `3^j`.  Hence

`sum_r k_m(r) <= s_a + sum_{j=1}^a 3^(a-j)`

`                 = (3^a+1)/2 + (3^a-1)/2`

`                 = 3^a`.

Pointwise one also has `1 <= k_m(r) <= a+1`.

Grouping exact `M`-moduli by square-free support as in M14, with

`b_S = sum_{sqf(m)=S} 1/m`,

therefore gives the general support-charge box and budget

`b_S <= q_S(r) <= (a+1)b_S`,

`sum_{r=1}^{s_a} q_S(r) <= 3^a b_S`.

This is the exact parameterized replacement for the M14 values

`14`, `4b_S`, `27b_S`.

## 3. Immediate test on the next same-support frontier

The next survivor with the same five-prime `M` support is

`34459425 = 3^4 * 5^2 * 7 * 11 * 13 * 17`.

Here `a=4`, so the M14 support box expands from `[b_S,4b_S]` to
`[b_S,5b_S]`, while the selected-fibre count and cross-fibre budget become

`s_4=41`,  `B_4=81`.

As a quick exact stress test, keep the *same* M14 affine weights `lambda_S`.
The exact minimum of

`rho(q) + sum_S lambda_S q_S`

on the enlarged `[b_S,5b_S]` box is

`C_5 = 273899/425425`.

Since the already verified M14 identity is

`sum_S lambda_S b_S = 144411/425425`,

the resulting summed margin is

`41*C_5 - 81*(144411/425425)`

`= -3928/3575 < 0`.

Thus the existing M14 affine certificate does **not** automatically lift from
`a=3` to `a=4`.  This is not a covering witness and not a no-go for the
Clique-Shearer method; it only identifies the next exact optimization target:
find a new affine support certificate for the enlarged factor-5 box, or prove
that no certificate in a specified affine class can yield positive
`41/81`-weighted margin.

This is the right next generalization problem before spending Codex budget on a
larger search.
