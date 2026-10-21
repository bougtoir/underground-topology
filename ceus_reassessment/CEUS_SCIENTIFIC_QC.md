# Gate 4 — independent scientific QC (CEUS run)

Audited 2026-10-10 against frozen outputs + new Gate-3 artifacts.

## Checklist

- Incumbent vs alternatives service requirements: candidate sets evaluated on identical demand/feasibility spec; incumbent admissible by estimand construction (VoF = mean_repl max(0, NPC(repl) − NPC(best feasible))). OK.
- VoF normalization/weighting: cluster VoF% = vof_mean/s1_npc_mean; zone VoF% is demand-weighted aggregate already in frozen registry — consistent use verified.
- Candidate-set gaps: "best" = best within the heuristic search set, stated; no global-optimality claim.
- Price year/discounting/LCC: unchanged frozen cost model (NPC life-cycle, consistent discounting); no DG double counting (S3 reported as supplementary upper bound only).
- Electrical constraints/AC validation: 672 feasible synthesized feeders, max|vm| err 0.0193 pu < 0.02, feasibility agreement 1.00 — validates linearized model on synthesized feeders only, stated as such.
- Spatial dependence/effective sample size: 589 clusters nested in 3 purposive zones; morphology analysis reported as descriptive Spearman summaries with sign-by-zone — no inferential zone claims, no pseudo-replicated p-value narrative. p values logged in the CSV for transparency but not used rhetorically.
- MC assumptions: 500 draws; sensitivity coverage documented (mc/tornado/mv120/mv200/t80/t130/rep24).
- 1% margin: described strictly as prespecified *practical* decision threshold (frozen spec file exists), never as a TOST/statistical equivalence result.
- Sign conventions: ΔNPC (secondary naive, incumbent-excluded) vs VoF (optional, nonnegative) consistently labelled; Kudamatsu −10% explicitly framed as estimand artifact.
- Morphology result honesty check: 94.1% of feasible clusters have VoF = 0; pooled positive correlations are tail-driven. Manuscript must say "value, where present, concentrates in larger/sparser/lower-density clusters" — NOT "morphology predicts savings". Zero-inflation disclosed in text and figure caption.
- Maps/figures: morphology scatter + decomposition figures generated programmatically from CSVs; no hand-inserted numbers.
- Unit audit: hull_area in km² via convex hull on projected x_m/y_m; edge lengths in m — consistent.

## Verdict

PASS — no unresolved material defect. Constraints to carry into drafting: zero-inflation disclosure; descriptive-only morphology language; modeled-network caveat in every relevant claim.
