# Milestone 72 — `(4,2,2,2,1,1)` reduces to four open exponent placements

For the sorted six-prime profile

\[
(4,2,2,2,1,1),
\]

there are 60 exponent placements at the minimal odd prime tuple
`(3,5,7,11,13,17)`.  Exact McNew–Setty evaluation leaves exactly nine with
`R>=1`; the other 51 are universally excluded by the M22 coordinate
monotonicity.

M72 now accounts for five of these nine direct survivors.  Thus the unresolved
part of this profile is reduced to exactly four exponent placements.

This is a six-prime reduction, **not** a closure of the full profile and not a
complete solution of Erdős Problem #7.

## 1. Nine direct survivors

The exact survivor list is

```text
(4,1,2,1,2,2)
(4,1,2,2,1,2)
(4,1,2,2,2,1)
(4,2,1,1,2,2)
(4,2,1,2,1,2)
(4,2,1,2,2,1)
(4,2,2,1,1,2)
(4,2,2,1,2,1)
(4,2,2,2,1,1)
```

The largest of the 51 directly killed placements is

\[
(2,4,2,2,1,1),\qquad
R=\frac{113145118}{113392125}<1.
\]

## 2. Three additional placements close by exact goodness certificates

For

```text
G1 = (4,1,2,1,2,2)
G2 = (4,1,2,2,1,2)
G3 = (4,1,2,2,2,1)
```

stage on `3^4` and apply exactly the M66 goodness construction.  The pointwise
quantity is

\[
g(q)=\min\left(\rho_{\rm full}(q),
\{\rho_C(q^0):\varnothing\ne C\subseteq J\}\right),
\]

augmented by the nonnegative M25 linear/diagonal/cross penalty tensor.  For
fixed non-special charges the special variables minimize as clipped rational
quadratics; the remaining function is separately concave, so all `2^15`
non-special endpoints suffice.

At the minimal prime tuple, the exact summed-goodness margins are

\[
G1:\quad
\frac{222591620880138610754590200697}
{940360333107412148411480000000}>0,
\]

\[
G2:\quad
\frac{58833770132728359473247079}
{388428312378232373547300000}>0,
\]

\[
G3:\quad
\frac{4103687720150083458129379}
{60262481625236672882100000}>0.
\]

All three exact endpoint minima occur at non-special corner bitmap `21569`.
M27 supportwise scaling transports these reference certificates to every
coordinatewise larger increasing prime tuple beginning with 3.  If the smallest
prime is not 3, the common anchor `(5,7,11,13,17,19)` already has `R<1` for all
three placements.

Therefore all three placements are completely excluded.

## 3. Import the already proved M70 and M71 placement theorems

M68–M70 already close the canonical placement

\[
(4,2,2,2,1,1),
\]

using exact double-square weighted activation certificates.  M71 closes

\[
(4,2,2,1,2,1),
\]

by distinguishing the `13^2` coordinate while retaining the exact weighted
`5^2` and `7^2` activations.

Thus five of the nine direct-survivor placements are now accounted for.

## 4. Exact remaining list

The only direct-survivor exponent placements not closed by the direct bound,
M72 goodness references, M70, or M71 are

\[
\boxed{
(4,2,1,1,2,2),\quad
(4,2,1,2,1,2),\quad
(4,2,1,2,2,1),\quad
(4,2,2,1,1,2).
}
\]

These are the next four targets for a full P4222 profile closure.

Files:

- `solver/m72_p4222_five_placements_closed.py` — exact reduction and the three
  new goodness references;
- `solver/test_m72_p4222_five_placements_closed.py` — regression checks.
