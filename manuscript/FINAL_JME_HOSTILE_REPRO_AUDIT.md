# FINAL JME HOSTILE REVIEW + REPRODUCIBILITY AUDIT

Target: Journal of Management in Engineering (ASCE) | Package: JME_submission_package_v1 | Audit date: 2026-10-21
Branch: devin/1792550201-jme-hostile-audit (base devin/ceus-supplement-promote, contains merged PR #708)
Canonical: manuscript/manuscript_jme.docx (sha256 9497ea37…, identical to package copy), cover_letter_jme.docx, Figures 1–6 PNG (300-dpi-generating scripts), ZIP + manifest.

## GATE 0 — Canonical inventory: PASS
- manuscript_jme.docx = package manuscript.docx byte-identical; 6 tables, 32 references, 6 figure captions.
- No remnants of Figure 7 / PV / S3 / rooftop / CEUS / SEGAN / CAIE / "previous version" / supplement (0 hits, incl. table cells).
- Cohort wording verified: 589 clusters → 554 feasible; AC validation = 672 feeder–scenario objects over 336 clusters (both-replicate-feasible), stated precisely; no claim of AC on all 554.
- Orphan media image7.png (stale DG figure) already removed from docx zip.

## GATE 1 — Independent hostile review: PASS (no FATAL/MAJOR; 3 MINOR fixed or logged)
Reviewer A (asset management): problem is genuinely an infrastructure-renewal investment decision (incumbent-admissible option value), JME precedent Ochs et al. 2014 cited correctly; contribution distinct vs 10 closest works (Zhang'25, Abhilash Bandam'21, Liu'25, Babli'25, Hadzilacos'00, Chahinian'19, Gilbert'21, Larsen'16, Fenrick'12, Camargo'13/feeder-routing set) — all differentiations stated without novelty absolutes.
Reviewer B (LV engineering): estimand implements stated choice set; denominators correct (554 feasible / 336 both-replicate / 127 non-degenerate hull); 1% margin is prespecified in config/ECONOMIC_EQUivalence_SPEC.yaml (frozen pre-classification) and called "practical-equivalence margin" not a formal TOST; negative Kudamatsu naive contrast correctly labeled incumbent-exclusion artifact; zero-mass/generalization caveats explicit.
Reviewer C (reproducibility): see Gate 2.
MINOR-1 [FIXED]: Figure 4 lacked the ±1% margin band its caption promised → axhspan added to scripts/p12d_figures_v4.py, figure regenerated, package updated.
MINOR-2 [FIXED]: public README still named SEGAN as target journal → journal-neutral title; repo name already journal-neutral.
MINOR-3 [logged, no action]: abstract "96% zero value" vs precise 95.7% — consistent rounding, acceptable.
Editor check: cover letter addressed to current JME Editor Qingbin Cui (verified ASCE editorial board, 2025 EOY review).

## GATE 2 — Public-data reproducibility: PASS at levels (i)+(ii) for all tested quantities; PARTIAL only for AC recompute and (iii) municipal rebuild
Clean clone bougtoir/underground-topology @ c42a923; fresh venv (requirements.lock.txt; pandapower 3.5.5).
- (ii) p07b_optimize_v2 re-run end-to-end: scenario_results_v2.csv and all 3 city cluster_results_v2.csv **byte-identical** to committed → VoF 0.0145/0.3935/0.2010%, 589/554, demands 38.4/9.5/10.7 MW, naive −10.06% all reproduced.
- p04_benchmark re-run: identical verdicts (CIGRE converged; Iwamoto non-convergent→excluded, matching manuscript).
- p11c_freeze_v3: **defect found** — required legacy analysis/benchmark_validation.csv while p04 now emits .json → pipeline crash. FIXED at source: script now falls back to the JSON (same two benchmark keys). Re-run reproduces manuscript_values_v3.csv exactly (185 values, identical).
- (i) Figure 3 canonical PNG had NO generating code (v4_fig2_topology_example.png was overwritten ad-hoc at commit cbc588f4; running p12d today emits a different, degenerate 2-line figure). FIXED at source: new scripts/p12e_route_length_fig.py regenerates the figure from cluster_results_v2.csv; re-derived content identical (19/554 >1 m, same cohort filter s2_feasible & n_s1_feas>0). Package Figure_3.png repointed to this generated file; p22 mapping updated.
- p09_ac_validation: re-run in progress at audit close (log so far: feasibility agreement 1.000, AC-vs-linear vdrop deltas consistent with committed AC_VS_LINEAR_VALIDATION.csv). Committed CSV itself matches manuscript (max|vm| 0.0193 pu ≤ 0.02 tol). Classified PARTIAL-pending rather than claimed.
- (iii) full rebuild from municipal/OSM raw: not attempted (data/raw pinned with sha256; would be multi-hour); level (ii) is the tested level — stated, not overclaimed.

## GATE 3 — Data–text–figure single-source: PASS after repairs
- Every headline number traced to canonical CSVs: Table 2↔scenario_results_v2.csv; Table 3↔CEUS_BOUNDARY_SENSITIVITY.csv; Table 4↔CEUS_ZERO_MASS_SUMMARY.csv; Table 5↔MORPHOLOGY_CORRELATIONS_CORRECTED.csv (all ρ, adjusted ρ, n: exact); Table 6↔CEUS_SPATIAL_DIAGNOSTICS.csv; inline text matches.
- Figure files: all 6 package PNGs provenance-verified (sha256 == generating-source files or regenerated above); first-mention order F1,T1,F2,T2,F3,F4,T3,T4,F5,T5,T6,F6 sequential; captions match content after Figure-4 fix; Japan-map geoBoundaries/Natural Earth attribution intact in Fig 2 caption.
- docx: 2 native OMML equations; no residual LaTeX; no CJK/full-width characters; no hardcoded result values in figure scripts (p21 text-patch constants match frozen values).

## GATE 4 — Bibliography & citation ecology: PASS
- 29 DOI references all resolve via Crossref; first-author + year verified (29/29 OK). 3 municipal-office URL refs are gray literature, cited in text.
- Every in-text citation maps to exactly one reference and every reference is cited (incl. Abhilash Bandam 2021, Ochs 2014, three City Office items).

## GATE 5 — Minimal repair & submission QC
- Repairs applied: p11c JSON fallback; p12e figure generator; p12d 1% band; README journal-neutral; package Figure_3/Figure_4 updated; ZIP + manifest rebuilt.
- Fees: ASCE specialty journals are hybrid — OA optional (APC $3,000 CC BY / $2,750 CC BY-NC-ND); no mandatory page charges on the subscription route → **$0 mandatory author fee verified** (ASCE Author Center, checked 2026-10-21).
- Cover letter: first-person singular, JME-fit framing, editor name current, author/affiliation placeholders retained by design.
- Final adversarial read of SAVED artifacts: done (docx text + package files + rendered figures).

## FINAL VERDICT: SUBMIT READY (pending user approval; do not auto-submit)
Unresolved-by-design items: author name/affiliation placeholders to fill at submission; level-(iii) municipal rebuild untested (data/raw pinned); p09 re-run still completing at audit close — committed AC table already consistent with manuscript.

Change log (this audit): scripts/p11c_freeze_v3.py (JSON fallback), scripts/p12d_figures_v4.py (band), scripts/p12e_route_length_fig.py (new), scripts/p22_jme_package.py (Figure_3 source), README.md (journal-neutral), figures/v4_fig3_delta.png + ceus_fig_routelength.{png,tiff} (regenerated), JME package Figure_3/Figure_4 + ZIP + manifest.
