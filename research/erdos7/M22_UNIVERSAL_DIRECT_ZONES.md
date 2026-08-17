# Milestone 22 — universal direct-bound zones for six odd primes

Milestones 20–21 excluded a substantial finite down-set of exponent profiles.  The same six-coordinate McNew–Setty bound has a stronger feature that was not yet used explicitly: its coordinate monotonicity is uniform for **arbitrary positive exponents**.

Let

\[
N=\prod_{i=1}^6 p_i^{a_i},\qquad 3\le p_1<\cdots<p_6
\]

with six distinct odd primes, and write

\[
x(p,a)=\sum_{j=1}^a p^{-j}.
\]

For six coordinates the full-divisor density bound is

\[
R=e_1-e_3-e_4+2e_5+9e_6.
\]

Whenever `R<1`, `N` is noncovering.

## 1. Uniform monotonicity for arbitrary exponents

For every coordinate,

\[
\frac{\partial R}{\partial x_i}
=1-e_2(y)-e_3(y)+2e_4(y)+9e_5(y)
\ge 1-e_2(y)-e_3(y),
\]

where `y` is the other five coordinates.  For every finite exponent,

\[
x(p,a)<\frac1{p-1}.
\]

Hence the five largest possible remainder coordinates are bounded by

\[
U=\left(\frac12,\frac14,\frac16,\frac1{10},\frac1{12}\right).
\]

Exactly,

\[
e_2(U)+e_3(U)=\frac{721}{1440},
\]

so throughout the entire six-odd-prime exponent domain

\[
\boxed{\frac{\partial R}{\partial x_i}\ge\frac{719}{1440}>0.}
\]

Thus `R` increases with every prime-power charge, with no upper bound on the exponents required.

## 2. Every exponent at most two

If

\[
1\le a_i\le2\qquad(1\le i\le6),
\]

then monotonicity puts the worst case at

\[
(p_1,\ldots,p_6)=(3,5,7,11,13,17),\qquad(a_1,\ldots,a_6)=(2,2,2,2,2,2).
\]

At this exact anchor,

\[
R=\frac{21635289362}{21718371675}
=1-\frac{83082313}{21718371675}<1.
\]

Therefore

\[
\boxed{\max_i a_i\le2\Longrightarrow N\text{ is noncovering}.}
\]

This single statement contains all 64 labelled `{1,2}` exponent assignments and, after sorting, all seven count-of-squares profiles from square-free through `(2,2,2,2,2,2)`.

## 3. At most one repeated prime, with arbitrary exponent

Suppose five exponents equal `1`, while the remaining exponent is arbitrary.  If the repeated prime is the `i`-th ordered prime, bound its charge by `1/(p_i-1)` and the five simple coordinates by `1/p_j`.  Monotonicity again reduces to the six smallest odd primes and only six possible positions for the repeated coordinate.

The exact six limiting values are

\[
\frac{90}{91},\quad
\frac{409}{462},\quad
\frac{10492}{12155},\quad
\frac{98786}{116025},\quad
\frac{953}{1122},\quad
\frac{9253}{10920}.
\]

Their maximum is `90/91<1`.  Hence, for **every** positive exponent `A`,

\[
\boxed{(A,1,1,1,1,1)\text{ in any prime position is noncovering}.}
\]

This is an unbounded exponent ray, not merely a finite profile down-set.

## 4. One arbitrary exponent on the third-or-later prime, all others at most two

There is also a larger rank-sensitive zone.  Suppose one distinguished exponent is arbitrary and is attached to the third-smallest prime or later, while all other five exponents are at most `2`.

For the distinguished coordinate use the limiting charge `1/(p_i-1)`; for every other coordinate use the exponent-two charge `(p+1)/p^2`.  The worst prime tuple is again `(3,5,7,11,13,17)`.  Enumerating the four possible distinguished ranks `i=3,4,5,6`, the maximum occurs at `i=3` and equals

\[
\frac{1593178541}{1595635470}
=1-\frac{2456929}{1595635470}<1.
\]

Therefore

\[
\boxed{
\begin{gathered}
\text{if an arbitrary exponent is carried by }p_i\text{ with }i\ge3,\\
\text{and all other exponents are }\le2,
\end{gathered}
\Longrightarrow N\text{ is noncovering}.}
\]

All constants and the six/four finite position scans are checked with exact `Fraction` arithmetic in `solver/m22_universal_direct_zones.py` and its tests.  These are internal rigorous theorem candidates pending independent literature/novelty review; they do not solve the general odd distinct covering-system problem.
