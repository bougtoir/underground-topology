# FINAL HANDOFF — feasible-cohort CEUS revision (2026-10-10)
Commit: a387c66db on devin/1791669486-caie-retarget (PR #656).
Quantitative changes vs prior package:
- Cohort: 554/589 electrically feasible (s2_feasible flag); 35 infeasible
  excluded via ledger; 9 infeasible rows carried vof>0 and are removed from inference.
- Positive VoF: 26/554 feasible (sano 3/360, kudamatsu 14/88, yasu 9/106);
  pooled zero share 95.3% (was ~94% over 589 with contamination).
- Morphology headline DOES NOT SURVIVE: rank-residual adjustment for terminal
  count collapses all extent/sparsity rhos to ~0 -> cluster-size confounding.
  Density non-replicable across supports (unchanged finding).
- Primary VoF estimand (0.01/0.39/0.20%) and all electrical numbers UNCHANGED.
- Horizon: 40-year verified; no 30-year prose remains.
Gate outcome: CEUS MAJOR REVISION REMAINS -> package is internally consistent and
  submission-viable as a humbler contribution (estimand + gating pipeline +
  honest exploratory morphology); morphology no longer carries the abstract.
Deliverables: CEUS_manuscript_folder_FEASIBLE_REVISED.zip;
  manuscript/manuscript_ceus_final.docx; inline docx; audits in ceus_reanalysis/.
Unresolved: CEUS-fit judgment call rests with author (power-eng method paper in
  an urban-systems journal); Clarivate primary JCR check still manual.
