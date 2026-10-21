# Feasibility cohort audit (Gate 1)
Authoritative flag: s2_feasible in {city}/cluster_results_v2.csv (one row per
cluster; unique (city,cluster); no replicate rows).
Verified counts: sano 360/385 feasible (25 infeasible), kudamatsu 88/96 (8),
yasu 106/108 (2) -> pooled 554/589 feasible, 35 infeasible. EXACTLY reproduces
the claimed counts.
Positive VoF on infeasible clusters: 9 (sano 5, kudamatsu 4, yasu 0) — these
vof_mean>0 values exist because the optimizer found cheaper but INFEASIBLE
redesigns; they are ineligible under the optional estimand and were silently
inflating the earlier pooled morphology correlations and the 35-positive count.
See EXCLUSION_LEDGER.csv (35 rows; not deleted, excluded from inference).
Eligible cohort: s2_feasible==True AND valid paired S1/S2 and non-null vof_pct
-> n=554. Positive VoF: 26 (sano 3/360, kudamatsu 14/88, yasu 9/106).
