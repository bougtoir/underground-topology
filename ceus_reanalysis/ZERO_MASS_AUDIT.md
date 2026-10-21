# Zero-mass audit (Phase 2) — analysis/CEUS_ZERO_MASS_SUMMARY.csv
Positive-VoF clusters: sano 8/385 (2.1%), kudamatsu 18/96 (18.8%), yasu 9/108 (8.3%)
-> pooled zero share 94.1%, but city-level zero shares differ widely (not pooled-noise).

Estimand dictionary:
- E1 = Pr(VoF% > 0 | city): incidence, estimated as positive share per city (n=589).
- E2 = E[VoF% | VoF% > 0, city]: conditional magnitude, median reported (0.21-0.96%).
- E3 = pooled morphology association: Spearman rho of descriptors vs vof_pct on ALL
  clusters (zero+positive), tail-driven; disclosed as such.
Zeros are substantive (binding feasibility), not numerical tolerance: no near-zero
clipping was applied; s1==s2 infeasible-vs-feasible split recorded in s2_feasible.

Honesty constraints applied: only 35/589 positive rows -> no hurdle/ZINB fit; two-part
reporting is descriptive (shares, medians, maxima) + rank correlations on the pooled
sample. Ties are extensive (94% zeros) -> Spearman rho with ties is the declared
estimand; p-values are permutation-level at best and reported with that caveat.
