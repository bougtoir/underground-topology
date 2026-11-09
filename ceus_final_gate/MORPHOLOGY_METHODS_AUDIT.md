# Morphology methods audit (Gate 2)
- terminals self-adjusted rho 0.787: degenerate 0/0 residual computation —
  recorded as artifact, CSV now carries NA; manuscript Table 3 shows "—".
- Rank-residual partial Spearman documented: residual of rank(x) and
  rank(vof_pct) on rank(terminals), Spearman of residuals. Tied ranks handled
  by scipy default (average ranks); 95.7% zeros make pooled rho a joint
  occurrence+magnitude summary — text distinguishes two parts.
- tld: endogenous post-optimization descriptor (shares construction with
  estimand); adjusted rho 0.78 flagged as internal diagnostic, excluded from
  morphology-claim passages. Denominators: 554 primary / 127 non-degenerate
  hull / 296 with internal road edges — all in SAMPLE_DENOMINATOR_AUDIT.
