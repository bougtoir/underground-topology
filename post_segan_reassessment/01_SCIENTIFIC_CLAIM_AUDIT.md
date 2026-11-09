# 01 — Scientific contribution audit

## Research question, unit, estimand

- Question: at overhead→underground renewal of LV distribution, is re-optimizing feeder
  topology/conductor sizing worth more than like-for-like replacement?
- Unit of analysis: transformer-zone clusters (415 V feeders, ~150 kVA) reconstructed on the
  municipal road graph of three Japanese municipalities (Sano, Kudamatsu, Yasu).
- True estimand: VoF = mean over reconstruction replicates r of
  max(0, NPC(S1_r) − min(NPC(S1_r), NPC(S2))) — the value of *optional* redesign with the
  incumbent admissible; nonnegative by construction; not a global-optimality claim.
- Optimization structure: weighted Steiner-tree synthesis + per-edge discrete conductor
  sizing + frozen electrical feasibility gates (≤6% drop, ampacity, 150 kVA loading,
  radiality), linearized power flow AC-validated on synthesized feeders, Monte-Carlo cost
  sweep, ensemble reconstruction to propagate unobserved-legacy uncertainty.

## A. Known concepts (not new)

- Steiner-tree network synthesis on road graphs (Hwang & Richards; Kou et al.)
- Discretized conductor selection (Tram & Wall); feeder routing/reconfiguration
  (Baran & Wu; Samui et al.; Kumar et al.; Camargo et al.)
- LinDistFlow linearized power flow + pandapower AC benchmark
- Life-cycle NPC evaluation under asset-management framing (Ross)
- OSM-derived demand/topology geography (Haklay & Weber; Abhilash et al.)

## B. Potentially new combination/application (increment of this paper)

1. Renewal-window estimand: quantifying redesign value as a nonnegative option (incumbent
   admissible) rather than a forced S1-vs-S2 comparison — the −10% Kudamatsu artifact
   demonstrates that the choice of estimand, not the physics, produced prior-looking large
   savings.
2. Legacy reconstruction ensemble: treating the unobserved incumbent as a distribution of
   feasible reconstructions and propagating that uncertainty into the cost contrast
   (vs single assumed topology in synthetic-feeder work).
3. Feasibility-first audit recipe: showing that ignoring coincidence/voltage/ampacity gates
   manufactures fictitious headroom (~350 kW undiversified loads → double-digit drops).
4. Municipal-scale application on three complementary data tiers with full raw-data
   provenance.

## C. Results newly established within this study

- VoF 0.01–0.39% of NPC across 554 feasible clusters / 58.6 MW modeled demand; all inside
  prespecified 1% practical margin → economically_equivalent classification.
- Like-for-like renewal is a defensible LV default *within the modeled design space*.
- ΔNPC sign instability under the LV/MV boundary assumption (documented sensitivity).
- AC-vs-linear validation on 672 synthesized feeders: max |vm err| 0.0193 pu, agreement 1.00.

## D. Claims NOT supported (must not be made)

- Actual utility incumbent superiority / nationwide optimality (topologies reconstructed,
  not observed).
- Any direct smart-grid operational performance (the SEGAN editor was right: none exists).
- Statistical equivalence in the TOST sense: the 1% margin is a model-based decision rule;
  uncertainty is propagated via scenarios/MC, not formal equivalence testing.
- Causality about Japanese utility practice; empirical observation of pole-to-pole routing.
- Savings on MV-served demand (excluded by design; cancels in contrasts).

## Novelty strength (honest)

Moderate: the contribution is a decision-analysis/measurement framing (estimand design +
feasibility gating + reconstruction uncertainty) yielding a bounded negative result, applied
to real municipal geographies. It is NOT a new algorithm or theorem. Its closest conceptual
home is infrastructure planning / asset-management decision support, not smart-grid
operation — consistent with the SEGAN editor's characterization.
