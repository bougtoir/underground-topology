# JIS Semantic Code Audit

Scope: canonical pipeline `scripts/p07b_optimize_v2.py` (optimisation and VoF), `scripts/p09_ac_validation.py` (AC validation), outputs `analysis/scenario_results_v2.csv`, `analysis/CEUS_ZERO_MASS_SUMMARY.csv`, `analysis/AC_VS_LINEAR_VALIDATION.csv`, cluster-level `data/processed/<zone>/cluster_results_v2.csv`, configs `config/ENGINEERING_FEASIBILITY_SPEC.yaml`, `config/ECONOMIC_EQUIVALENCE_SPEC.yaml`, `config/study.yaml`. Independent checks: `tests/test_vof_semantics.py` (6 unittest cases, all pass) and `scripts/p31_ac_clusterload_check.py` (AC re-check with optimisation-consistent loading; canonical file untouched).

Source of truth: private repo `bougtoir/wip`, subdirectory `underground_topology_segan/`, branch `devin/ceus-supplement-promote` at merge commit `d49bb52a2` (PR #714 merged into it; tree identical to `d5ce3a086`, the commit mirrored to public `bougtoir/underground-topology` main). No newer scientific work exists on any other branch or open PR.

## 1. Baseline freeze (machine outputs vs. expected values)

| Quantity | Expected | Observed (source) | Status |
|---|---|---|---|
| Total clusters | 589 | 385 + 96 + 108 = 589 (`scenario_results_v2.csv` `clusters`) | match |
| Electrically feasible clusters | 554 | 360 + 88 + 106 = 554 (`clusters_feasible`) | match |
| Modeled demand by zone | 38.4 / 9.5 / 10.7 MW | 38.44 / 9.50 / 10.69 MW (`lv_demand_kw`) | match — **but this is demand of all 589 clusters** (see D1) |
| Primary VoF | 0.01 / 0.39 / 0.20 % | 0.01449 / 0.39354 / 0.20098 % (`vof_pct`) | match |
| Zero-VoF share | ≈95.7 % | 1 − 24/554 = 95.67 % (positive 3/13/8, `CEUS_ZERO_MASS_SUMMARY.csv`) | match (see D2) |
| AC cohort | 672 objects / 336 clusters | 672 rows = 336 clusters × {S1, S2} | match (see D3) |
| AC max \|ΔV\| | ≈0.0193 pu | 0.019267 pu (`vm_abs_err`) | match |
| AC feasibility agreement | 1.000 | 672/672 rows `feas_lin == feas_ac` | match |
| AC max relative loss error | ≈0.226 | 0.2258 (`loss_rel_err`) | match |
| Secondary naive contrast, Kudamatsu | ≈ −10.06 % | −10.062 % (`ltp_pct`) | match |

## 2. Estimand-by-estimand audit

### VoF (primary)
1. **Definition** (code, p07b lines ~250–256): for each feasible cluster *c* and each ampacity-feasible incumbent replicate *r* (reconstruction ensemble), VoF<sub>c,r</sub> = max(0, NPC(S1<sub>c,r</sub>) − min<sub>k</sub> NPC(S2<sub>c,k</sub>)), where S2 candidates are weighted Steiner trees (loss weights 0,1,3,10,30,100) with per-edge conductor optimisation; VoF<sub>c</sub> = mean over replicates. Matches the manuscript equation (incumbent retained in the choice set ⇒ min(S1, S2)).
2. **Sign/direction**: positive = re-layout saves money; ≥ 0 by construction (tested). Non-negativity is a mathematical property, not a finding.
3. **Units/scales**: JPY net present cost, 40-year horizon, 3 % discount, annuity factor `ADF`; zone VoF% = 100 × ΣVoF<sub>c</sub> / ΣNPC(S1)<sub>c</sub> over feasible clusters — a **cost-weighted pooled ratio**, not a mean of cluster ratios. Manuscript must say "share of zone-level like-for-like NPC".
4. **Aggregation/denominator**: feasible clusters only (554); trivial single-customer clusters contribute TRM_NPC to the denominator and 0 to the numerator (D2). Re-derived exactly by the test.
5. **Comparison set**: S1 = reconstructed incumbent topology, 150 mm² fixed conductor; S2 = redesigned topology with optimised conductors. VoF therefore bundles topology *and* conductor flexibility (S2 vs S1 differ in both). The ablation columns `s2f_npc` (topology-optimised, conductor-fixed) exist but are secondary. Manuscript must not attribute VoF to topology alone.
6. **Inference unit**: cluster (transformer zone); zones are three purposively selected study areas — no population inference.
7. **Interpretation**: all three zone VoF values lie inside the ±1 % equivalence margin → like-for-like renewal is economically equivalent at zone scale *under this model*; individual clusters reach 5.1 % (Kudamatsu) and 6.1 % (Yasu).

### Feasibility gates
Code: `feasible = vd ≤ 6.0 and coinc_kva ≤ 150`; ampacity enforced by returning `None` (fixed 150 mm²: any edge current > 350 A) or by restricting conductor sizes; radiality via tree construction (`nx.is_connected` on tree edgelists; Steiner output pruned to a tree); coincident demand = raw × 0.6; PF 0.9; 415 V line-to-line; aluminium ρ = 2.826×10⁻⁸ Ω·m; voltage drop computed as resistive √3·I·R cumulative along BFS order (reactance ignored in the gate). A cluster is "feasible" if the best S2 is feasible and ≥1 incumbent replicate is ampacity-feasible. Verified: in all 554 feasible clusters, max incumbent drop ≤ 6 % (max 4.93 %) and transformer loading is common to S1 and S2, so every incumbent replicate in the feasible set also passes all gates (test `test_feasible_incumbents_respect_gates`).

Caveat: S2 is the *cheapest* ampacity-feasible candidate; if it violates the drop gate the cluster is excluded even if a dearer candidate is feasible (35 clusters excluded overall). This is conservative for VoF and is stated in the manuscript.

### Secondary naive contrast (ΔNPC without incumbent)
`ltp_pct` = 100 × Σ(S1 − S2)/ΣS1; can be negative (Kudamatsu −10.06 %) because it forces re-layout even when the incumbent is cheaper. Reported only as an artifact of excluding the incumbent.

## 3. Defects and discrepancies found

| ID | Finding | Evidence | Severity | Resolution |
|---|---|---|---|---|
| D1 | Manuscript (JME/CEUS text) says "554 feasible feeder clusters serving 58.6 MW". 58.6 MW is the demand of **all 589** clusters; the 554 feasible clusters serve **49.6 MW** (31.78 + 7.57 + 10.21). | `p07b` line `lv_demand_kw=rc["raw_kw"].sum()` (all clusters); test `test_demand_denominators` | Major (wrong denominator in abstract) | Corrected in JIS text: "589 clusters (58.6 MW) … 554 feasible clusters (49.6 MW)" |
| D2 | 218 of the 554 feasible clusters (175/19/24) are **single-customer** zones with no topology choice; VoF = 0 by construction. The "95.7 % zero" statistic mixes structural and empirical zeros. Among the 336 clusters with a genuine topology choice, 312 (92.9 %) have zero VoF; zone VoF over non-trivial clusters is 0.018 / 0.401 / 0.209 %. | `p07b` degenerate-cluster branch; test `test_counts_and_vof_pct` | Major (interpretation) | Both denominators reported; conclusions unchanged (still ≪1 %) |
| D3 | AC validation cohort is not byte-identical to the evaluated plans: p09 loads the S1 replicate with demand at **all nodes on the reconstructed tree** (including customers assigned to neighbouring clusters), and rebuilds its own S2 Steiner tree. The reported AC maximum drop (11.36 %, linear 9.43 %) belongs to two such over-loaded S1 surrogates (Sano clusters 190 and 375) that are infeasible in **both** models; in the optimisation those incumbents have 0.84 % and 2.50 % drop. | `p09` line `dem_cc = {t: … for t in T.nodes}` vs `p07b` `dem_c_cluster`; `AC_VS_LINEAR_VALIDATION.csv` rows 178, 350 | Moderate (explains the "6 % gate vs >6 % AC value" discrepancy; does not invalidate model-form agreement) | AC result described as a **model-form validation** of the linearised voltage/loss calculation on 672 feeder–scenario objects (agreement 1.000; \|ΔV\| ≤ 0.0193 pu); the >6 % values are disclosed as gate-violating stress cases; optimisation-consistent re-check in §4 |
| D4 | The unit test suite `tests/test_electrical_model.py` exercises `scripts/electrical_model.py` (210 V single-phase spec in repo root), not the canonical `p07b` inline model (415 V, `config/` spec). | test imports | Minor (test coverage gap) | New `tests/test_vof_semantics.py` checks canonical outputs; noted in QC |
| D5 | VoF combines topology and conductor re-sizing (S2 optimises both). | p07b `npc_value(..., True)` for S2, `False` for S1 | Moderate (attribution) | Manuscript defines VoF as value of re-layout *with* re-sizing; S2f ablation mentioned |

## 4. Optimisation-consistent AC re-check (D3)

`scripts/p31_ac_clusterload_check.py` reruns p09 with the S1 replicate loaded only at the cluster's own terminals (the loading used by p07b); S2 handling is unchanged. Output: `analysis/JIS_AC_CLUSTERLOAD_CHECK.csv`, `analysis/JIS_AC_CLUSTERLOAD_REPORT.md`.

| Statistic | Canonical p09 (all-node S1 loading) | Optimisation-consistent (cluster-terminal S1 loading) |
|---|---|---|
| Feeder–scenario objects / clusters | 672 / 336 | 672 / 336 |
| Non-converged | 0 | 0 |
| Feasibility agreement (linear vs AC, 6 % gate) | 1.000 (670 both feasible, 2 both infeasible) | 1.000 (672 both feasible) |
| max \|V_AC − V_lin\| | 0.0193 pu | 0.0056 pu |
| max relative loss error | 0.226 | 0.079 |
| max voltage drop, linear / AC | 9.43 % / 11.36 % | 4.27 % / 4.82 % |

Interpretation: under the loading actually used for the decision, every incumbent and redesign object passes the 6 % gate under full AC power flow with ≥1.18 percentage points of margin; AC drops exceed the resistive linear estimate by at most ~0.55 pp (reactance and nonlinearity), which the gate margin absorbs. The canonical file is retained as a conservative stress test. The JIS manuscript reports the optimisation-consistent check as the primary AC validation and the canonical (over-loaded) run as a stress case, with both scripts public.

## 5. Sensitivity evidence relevant to interpretation

- 21 engineering-assumption variants (`ENGINEERING_ASSUMPTION_SENSITIVITY.csv`: LV/MV threshold 120/200 kW, cluster target 80 kW, coincidence 0.5/0.7/0.8, 24 replicates): zone VoF ranges 0.001–0.947 %; all inside the 1 % margin; maximum drop among feasible clusters ≤ 5.91 %.
- Monte-Carlo (500 draws, `sensitivity_mc_v2.csv`) and tornado (`sensitivity_tornado_v2.csv`: discount rate, energy price, horizon, load factor, O&M, cost multiplier) are computed for the **naive contrast**, not for VoF. They show Kudamatsu's naive contrast negative in all draws (5–95 %: −0.58 to −0.31 bn JPY) and Sano/Yasu positive but < 0.25 %. The manuscript must not describe them as VoF uncertainty intervals. Economic categories of `ECONOMIC_EQUIVALENCE_SPEC.yaml` are applied to the point VoF and the assumption variants only.

## 6. Verdict

No defect changes the primary conclusion (zone VoF ≪ 1 % margin; value concentrated in 24 clusters). D1–D3 are reporting/interpretation defects corrected in the JIS manuscript; no release-grade rebuild is required. Protocol ↔ code ↔ output consistency verified for gates, estimand, sign, units, aggregation and denominators.
