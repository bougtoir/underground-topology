# Gate decisions — feasible-cohort reanalysis (2026-10-10)
Gate 0 PASS: CEUS eligibility unchanged (subscription $0, JCR Q1 8.3); branch devin/1791669486.
Gate 1 PASS: counts verified exactly 360/88/106 -> 554/589 feasible (s2_feasible flag in
  cluster_results_v2; unique city+cluster key, one row per cluster, no replicate
  duplication). EXCLUSION_LEDGER.csv: 35 infeasible, 9 with vof_mean>0 (sano 5,
  kudamatsu 4) — values existed but are ineligible under the optional estimand
  (their S2 rows are infeasible; VoF>0 there reflects infeasible redesigns, not
  admissible option value). Removed from primary inference, not deleted.
Gate 2 PASS: descriptor validity as in prior audit; feasible-cohort degenerate-hull
  count = 127 non-degenerate rows for hull density; buffer support retained;
  buffer-distance robustness: single 100-m support kept (exploratory label; scale
  sensitivity noted as limitation rather than a grid hunt).
Gate 3 PASS: feasible cohort positives = 26/554 (sano 3/360, kudamatsu 14/88,
  yasu 9/106); zero share 95.3% pooled. Two-part reporting kept; no hurdle model.
Gate 4 CONDITIONAL->demotion: feasible-cohort pooled Spearman rhos drop
  (terminals 0.32, tld 0.37, span 0.29, hull_area 0.30 non-degenerate). Rank-residual
  adjustment for terminal count collapses ALL extent/sparsity associations to ~0
  (span -0.011, route/term -0.027, hull_area 0.006, road_density -0.192,
  mean_degree -0.289). CONCLUSION: morphology-VoF association is a cluster-SIZE
  effect, not an independent morphology effect -> demoted to exploratory/limitations.
  terminals-adjusted rho is not defined for terminals itself; tld is mechanically
  coupled to size and likewise not interpretable independently.
Gate 5 PASS: 40-yr primary horizon verified in config; prose already fixed.
Gate 6 CONDITIONAL PASS (revised contribution): morphology headline does NOT survive.
  Remaining CEUS contribution = geospatial reconstruction + incumbent-admissible
  VoF estimand + feasibility gating as a municipal screening pipeline; morphology
  analysis retained as honest exploratory finding showing size confounding.
  No false novelty claim; this is a legitimate (if humbler) CEUS contribution.
Gate 7-9: figures/tables/manuscript rebuilt on feasible cohort; no 589-feasible claims.
FINAL DECISION: CEUS MAJOR REVISION REMAINS — package is submission-consistent,
  but morphology moved from headline to exploratory; author should decide whether
  the humbler contribution still merits CEUS vs a more applied-energy venue.
