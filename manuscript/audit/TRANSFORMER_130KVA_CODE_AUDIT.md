# TRANSFORMER_130KVA_CODE_AUDIT (Gate 3)
Scripts: reconstruction scripts/p06b_reconstruct_v2.py (env: TAG, CLUSTER_KW,
NREP); optimization scripts/p07b_optimize_v2.py (env: TAG, INTAG, COINC;
transformer gate = ENGINEERING_FEASIBILITY_SPEC.feasibility.transformer.rated_kva
=150 kVA, not env-configurable until this audit added XFORM_KVA env override).
FINDING — the stored cluster_results_t130.csv is a STALE ARTIFACT from the
superseded v1 optimizer (scripts/p07_optimize.py), not from p07b:
- 78/302 (sano), 2/77 (kudamatsu), 10/86 (yasu) rows; every emitted row is
  single-terminal; vof_mean column absent. Current p07b always writes vof_mean
  (0.0 for singletons) — the missing column proves older code produced it.
- v1 silently skipped clusters with no feasible S1.5/S2 pair ('continue' at
  no_feasible branches), so multi-terminal rows were never written. The all-
  singleton file is a surviving subset, not a population property.
- clusters_t130.csv partitioning (302 clusters, fewer than v2's 385) also
  couples cluster size to the variant — parameter coupling defect.
VERDICT: not 'estimand undefined' and not robustness evidence — defective
stale artifact. Previous 'all qualifying clusters single-terminal'
explanation superseded by this audit.
TARGETED RERUN (minimal causal path, no re-optimization of baseline):
  XFORM_KVA=130 INTAG=v2 TAG=t130 scripts/p07b_optimize_v2.py
  reusing the frozen v2 reconstruction. Results: feasible sano 352/385,
  kudamatsu 82/96, yasu 97/108 (gate removes 8/6/9 vs 150 kVA); VoF%
  sano 0.0150, kudamatsu 0.3196, yasu 0.2258 — materially unchanged from
  baseline. Table 4 now carries real values; the rating is mildly binding.
Primary cohort and estimates unaffected (t130 is a sensitivity variant only).
