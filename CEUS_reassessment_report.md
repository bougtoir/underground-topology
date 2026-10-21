# CEUS gated reassessment — final report (2026-10-10)

## Gate outcomes

| Gate | Result |
|---|---|
| 0 Canonical state + financial eligibility | **PASS** — subscription route $0 to authors confirmed on the official CEUS ScienceDirect page (optional OA APC $4,280 only); JIF 8.3/JCR Q1 via publisher-displayed IF + two secondary sources (primary Clarivate check flagged for submission); scope plausible (geospatial decision support, infrastructure & facilities management); research-article route available |
| 1 Citation ecology + real novelty | **CONDITIONAL PASS** → cleared by Gate 3 — the CEUS-relevant increment (morphology-conditioned, feasibility-gated option value over reconstructed networks) is defensible; incumbent-admissibility is an estimand point, not sold as new theory |
| 2 Data validity + spatial identification | **PASS with transparent limitations** — tiers verified from files on disk (Sano pole-ID anchors, Kudamatsu geolocated anchors, Yasu roads/buildings only); metric CRS verified; purposive zones, no pseudo-replication, modeled-network framing |
| 3 Additional analyses | **Executed** — Priority A (morphology→VoF), F (cost decomposition), C (boundary sensitivity reuse); D/E excluded with logged reasons; no re-optimization runs |
| 4 Independent scientific QC | **PASS** — checklist in CEUS_SCIENTIFIC_QC.md; zero-inflation + descriptive-only language enforced |
| 5 CEUS fit reassessment | **PASS** — four-lens review in CEUS_FIT_REVIEW.md; drafting permitted with language discipline |
| 6 Package | **Built** — manuscript + all submission files + zip |

## New results generated (with provenance)

- `analysis/CEUS_MORPHOLOGY_CLUSTER.csv` — 589 feasible clusters × 9 morphology descriptors + VoF (from frozen `cluster_results_v2.csv` + processed zone geometry).
- `analysis/CEUS_MORPHOLOGY_CORRELATIONS.csv` — pooled Spearman ρ: area 0.38, span 0.32, route length/terminal 0.31, terminals 0.35, degree 0.27, edge length 0.23, coincident kW 0.19, demand density −0.31, TLD 0.32; sign consistent in all 3 zones; 94.1% of clusters have VoF = 0 (tail-driven relation, disclosed).
- `analysis/CEUS_BOUNDARY_SENSITIVITY.csv` — reused frozen mv120/mv200/t80/t130/rep24 variants.
- Figures: `ceus_fig_morphology`, `ceus_fig_decomposition`, `ceus_fig_pipeline` (PNG+TIFF).
- Code: `scripts/p15_ceus_morphology.py`, `p16_ceus_figures.py`, `p17_manuscript_ceus.py`, `p18_package_ceus.py`.

## Frozen results carried forward unchanged

VoF +0.0145%/+0.3935%/+0.2010%; naive ΔNPC +0.014%/−10.06%/+0.20%; AC validation 672 feeders, max|vm| 0.0193 pu, agreement 1.00; LV shares 74.7/55.1/53.4%; MC 500 draws; S1 family ratios ~1.00.

## Exact final research claim

At low-voltage scale, renewal-time re-layout has bounded optional value (<0.5% of life-cycle cost) under engineering feasibility gating and an incumbent-admissible estimand; residual value concentrates in larger, spatially sparser, lower-demand-density feeder clusters. The transferable contribution is the feasibility-gated reconstruction-plus-decision pipeline and a screening rule — not the magnitudes, which are modeled results for three purposive Japanese zones.

## Verdict

CEUS submission is appropriate: all hard gates passed; the package is complete but **not yet submission-ready** — author must fill identity fields, verify JCR on Clarivate, name-check the current EiC, and confirm the current Guide for Authors before upload.
