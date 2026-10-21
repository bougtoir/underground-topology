# 00 — Baseline audit (post-SEGAN rejection reassessment)

Date: 2026-10-10 (UTC). Analyst: Devin session devin-874a3ef9227b44cea36abe713bf8a448.

## Repository state

- Working repo: `bougtoir/wip`, directory `underground_topology_segan/` (private monorepo; all
  artifacts merged to `master`).
- Latest commit touching the project at audit time: `67d312fa067b2bb3d8a626b073b613957236b180`
  (2026-10-09 +0900) "SEGAN v4 review fixes: unclip negative ΔNPC in fig3, include
  data+requirements in package zip".
- Public mirror: `github.com/bougtoir/underground-topology` (name contains no journal name; no
  remapping needed for retargeting).
- The prompt names canonical source `bougtoir/underground-topology-segan`; the wip checkout is
  newer than the public mirror and is used as baseline. v4 manuscript text is reproduced
  verbatim from `scripts/p13d_manuscript_v4.py` → `manuscript/manuscript_draft_v4.docx`
  (extracted and diffed against builder source; consistent).

## Verified numerical freeze (from machine-readable outputs, not prose)

- `analysis/manuscript_values_v3.csv` is the authoritative value table.
- Primary estimand VoF (incumbent admissible, nonnegative): Sano +0.0145%, Kudamatsu +0.3935%,
  Yasu +0.2010% of S1 NPC — all inside the prespecified 1% practical margin →
  `economically_equivalent`.
- Secondary naive ΔNPC: Sano +0.014%, Kudamatsu −10.06%, Yasu +0.20%. Kudamatsu sign flips
  under MV-served threshold (200 kW → +0.27%; 120 kW → −2.21%): disclosed estimand/threshold
  artifact, never the primary claim.
- AC validation: `analysis/AC_VS_LINEAR_VALIDATION.csv` — 672 feasible synthesized feeders,
  all converged, max |vm err| 0.0193 pu (< prespecified 0.02), feasibility agreement 1.00.
  Scope: linearized-model validation on synthesized feeders only.
- LV demand coverage: 74.7% / 55.1% / 53.4% of total zone demand; MV-served demand excluded by
  design and cancels in contrasts.
- MC 500 draws; rep24 and leave-one-family-out stable (S1 family NPC ratios 1.000/1.006/1.004).

## Manuscript inventory (v4, submission-ready for SEGAN)

- `manuscript/manuscript_draft_v4.docx` — main text, numbered (Vancouver) citations,
  **12 references** (note: earlier handoff text claimed 27; actual v4 list = 12, all
  Crossref-verified in `analysis/references_verified.csv`… 12 DOI rows).
- `manuscript/manuscript_inline_v4.docx`, `manuscript/supplementary_material_v4.docx`,
  `cover_letter_v4.txt`, `highlights_v4.txt`, `declarations_v4.txt`.
- Figures v4 fig1–fig4 (+supp figS1), PNG+TIFF, 300 dpi. Tables 1–2 embedded.
- `SEGAN_submission_package_FINAL_v4.zip` present.
- Editorial decision: SEGAN-D-26-05388, desk rejection (EiC G. Chicco): "many of the
  discussions are in the domain of layout of network and application of smart grid network is
  limited… no discussion on proposed study on direct performance/operation of smart grid
  application." Interpreted as a scope-fit rejection, not a methods rejection.

## Mismatches / defects found at baseline (fed to Phase 8)

1. Manuscript uses "pre-registered" 4×; standing rule requires "prespecified" (the margin is a
   model-based decision rule, not a statistical equivalence test). Fixed in the CAIE variant.
2. Reference count is 12, not 27 — several communities are under-cited (undergrounding
   economics, feeder routing, synthetic-topology reconstruction). Material additions listed in
   02_CLOSEST_PRIOR_WORK_MATRIX.csv.
3. Abstract 249 words (counted from the extracted v4 text) — inside typical limits, trimmed
   for the new target.
4. `config/ECONOMIC_EQUIVALENCE_SPEC.yaml` is referenced in prose as an internal path; this is
   acceptable provenance but should become a supplement citation rather than a bare repo path.
5. SEGAN-specific framing ("sustainable energy", smart-grid adjacency, journal-directed cover
   letter/highlights) must be removed for retargeting.

## Files preserved

No SEGAN artifacts were modified. All retargeting lives in `post_segan_reassessment/` and new
`manuscript/*_caie.*` outputs plus `scripts/p13e_manuscript_caie.py`,
`scripts/p14e_package_caie.py`.
