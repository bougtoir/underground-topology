# Adjustment formula audit (Gate 2D/E)
Method: rank-residual partial Spearman. rank(x) and rank(vof_pct) each OLS-
regressed on rank(terminals); Spearman of residuals.
- "terminals adjusted for terminals" (earlier rho_adj=0.787): undefined —
  residual of rank(terminals) on itself is identically 0, so the residual
  correlation is 0/0 (degenerate). NOT a real number; the 0.787 was the raw
  self-correlation artifact of the implementation. Correct handling: shown as
  "—" in Table 3; dropped from inference.
- tld (topology divergence distance) adjusted rho 0.780: tld is computed from
  the reconstructed topology itself (post-optimization descriptor), and scales
  mechanically with cluster size/demand — it cannot be an exogenous urban
  morphology predictor. Demoted: reported as endogenous diagnostic only;
  not presented as an independent correlate.
