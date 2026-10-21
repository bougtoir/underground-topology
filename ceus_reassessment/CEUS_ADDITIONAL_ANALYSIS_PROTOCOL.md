# Gate 3 — prespecified additional analyses (frozen before observing results)

Frozen 2026-10-10. All analyses reuse existing frozen outputs plus geometric
descriptors computed from already-processed zone files. No re-optimization.

## Priority A — urban morphology → VoF (RUN)

- Question: does measurable urban spatial structure condition the
  feasibility-adjusted value of topology flexibility at feeder-cluster scale?
- Estimand: cluster-level VoF% = vof_mean / s1_npc_mean × 100 (feasible
  clusters only, s2_feasible=True or vof computable).
- Spatial unit: feeder cluster nested in zone (descriptive; within-zone
  spatial dependence acknowledged — no pseudo-replicated inference).
- Prespecified descriptor set (small, interpretable; from data/processed):
  1. n terminals (demand nodes)
  2. coincident demand kW
  3. cluster convex-hull area (km²) of member demand-node coordinates (x_m/y_m)
  4. demand spatial density = coinc_kw / hull area
  5. mean road-edge length (m) within cluster (edges among member nodes)
  6. mean node degree within cluster
  7. route compactness = s1_length_mean / terminals (m of incumbent-route
     length per demand node)
  8. incumbent spatial span = mean distance from cluster centroid to demand
     nodes (m)
- Method: pooled Spearman rank correlation per descriptor vs VoF% + scatter
  figure colored by zone + within-zone sign consistency. Report rho and n;
  flag spatial dependence; NO p-value-led claims.
- Decision threshold for main-text inclusion: |rho| ≥ 0.30 pooled OR
  consistent sign in ≥2 of 3 zones → a morphology-conditioning sentence in
  Results/Discussion; otherwise report as "no strong univariate morphology
  signal at cluster scale" (still a substantive bounded finding).
- Implementation: scripts/p15_ceus_morphology.py; outputs
  analysis/CEUS_MORPHOLOGY_CLUSTER.csv, analysis/CEUS_MORPHOLOGY_CORRELATIONS.csv,
  figures/ceus_fig_morphology.png/.tiff.

## Priority F — cost decomposition / frontier (RUN, reuse only)

- Reuse analysis/component_decomposition.csv + BENEFIT_DECOMPOSITION.csv
  (capex vs loss components of S1−S2). Render a per-zone decomposition
  figure (capex length component vs loss component vs VoF) →
  figures/ceus_fig_decomposition.png/.tiff. Distinguish nonnegativity of the
  option-value definition from its small empirical magnitude.

## Priority C — boundary/assumption sensitivity (RUN, reuse only)

- Reuse scenario_results_{mv120,mv200,t80,t130,rep24}.csv already computed:
  table of VoF% and ΔNPC% under boundary/parameter variants →
  analysis/CEUS_BOUNDARY_SENSITIVITY.csv. No new runs.

## Excluded (logged)

- Priority D (cross-zone/LOZO validation): only 3 zones; no independent
  geographic units → would be pseudo-validation. Excluded by design.
- Priority E (tier-degradation experiment): rerunning reconstruction with
  degraded anchors is a compute+design task beyond "minimal targeted reruns"
  and not identifiable cheaply; logged as future work, not silently implied.
- Priority B (conditional value map): partially covered by zone figure +
  cluster-level morphology outputs; a separate georeferenced value map adds
  cosmetic value only — excluded unless Gate 5 demands it.
