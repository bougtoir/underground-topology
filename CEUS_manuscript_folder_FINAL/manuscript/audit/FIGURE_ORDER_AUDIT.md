# FIGURE ORDER AUDIT
Before (inline): embedded order 1,2,4,3,6,5 — cause: two figure
references share a single Results paragraph (Fig3/Fig4; Fig5/Fig6) and
the p18 inserter stacked later insertions first.
Fix: reversed insertion order in p18; inline rebuilt.
After: IMG+caption sequence = 1,2,3,4,5,6 (verified programmatically).
First-citation order in canonical text: 1(Intro/estimand), 2(Methods),
3,4 (Results par), 5,6 (Results par) — consecutive; PASS.
Exactly six image-caption pairs in body; separate caption list retained
at end for the separate-figure submission copy; no duplicates/orphans.
Normal manuscript: untouched (captions-only list is correct).
