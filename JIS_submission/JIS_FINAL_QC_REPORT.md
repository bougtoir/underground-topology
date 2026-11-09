# JIS Final QC Report

Date: 2026-11-09. Branch `devin/1794233571-jis-retarget` of private `bougtoir/wip` (subdirectory `underground_topology_segan/`), based on source of truth `devin/ceus-supplement-promote` @ `d49bb52a2` (tree = `d5ce3a086`, mirrored on public `bougtoir/underground-topology`).

## Decision: **CONDITIONAL SUBMIT**

The manuscript is scientifically defensible, fits JIS, and complies with the verified ASCE rules. It is not `SUBMIT` only because author-supplied items are missing (affiliation, postal address, email) and because three external checks must be made by the author in Editorial Manager (below). Neither `SCOPE NO-GO` nor `SCIENTIFIC NO-GO` is triggered.

## Integrated assessment

| Dimension | Evidence | Result |
|---|---|---|
| Scientific validity | `JIS_SEMANTIC_CODE_AUDIT.md`: estimand, gates, signs, units, aggregation and denominators verified against code and outputs; `tests/test_vof_semantics.py` (6 tests incl. synthetic VoF) + `tests/test_electrical_model.py` (8) → 14/14 pass | PASS. Defects D1 (58.6 MW denominator), D2 (218 structural zeros), D3 (AC loading mismatch) corrected in the JIS text; optimisation-consistent AC re-run added (`scripts/p31_ac_clusterload_check.py`). No defect changes the conclusion |
| Journal fit | `JIS_SCOPE_AND_LITERATURE_FIT.md`: official aims & scope (energy distribution, uncertain information, economic flexibility) and 15 Crossref-verified JIS precedents | GO. Novelty constrained to the renewal-window, incumbent-admissible screening estimand |
| Guideline compliance | `JIS_AUTHOR_GUIDELINES_AUDIT.md` (27 items; archived official ASCE pages, live pages blocked by HTTP 403) | PASS for all verifiable items; JCR quartile `UNVERIFIED` (not needed for submission) |
| Length | 24 rendered double-spaced pages (text, references, captions, tables) + 5 figures (1 page each) = 29 ≤ 30 | PASS (conservative count) |
| Manuscript consistency | All numbers generated at build time by `scripts/p32_manuscript_jis.py` from CSV outputs; builder assertions on abstract/PA length, citation ↔ reference matching, sequential Fig./Table citation, decomposition claim | PASS |
| References | `JIS_REFERENCE_AUDIT.md`: 36 references, 30 DOI records match Crossref on all fields, 1 resolved metadata anomaly, 5 web/data citations; 16 JIS papers | PASS |
| Figures/tables | `JIS_FIGURE_TABLE_CONSISTENCY.md`: 5 figures (TIFF, 300 dpi, ≥ 8 pt, grayscale-safe) supplied separately, 1 supplemental figure, 6 editable tables | PASS |
| Word quality | `analysis/JIS_DOCX_QC.json` (all checks PASS): Times New Roman 12 pt, black, no character spacing, 3 native OMML equations, no embedded images, no .dot/.dotx, unnumbered headings in ASCE order, line and page numbers; PDF inspected visually | PASS |
| Declarations | Standalone "Data Availability Statement" (two ASCE verbatim options + public/third-party/non-redistributable distinction + data citations), Acknowledgments (no funding), standalone "Disclosure of AI Tool Use" reflecting actual use | PASS |
| Reproducibility | Public repo + documented sources reproduce outputs (canonical rebuild verified in the prior JME audit; JIS changes add only post-processing, an AC variant, tests and document builders, all re-run here) | PASS (no release-grade rebuild needed; no upstream defect) |
| Adversarial review | `JIS_HOSTILE_REVIEW.md`: 17 objections; 0 critical open; #3 and #5 mitigated by disclosure; #17 administrative open | PASS with disclosed residual risk |
| Cover letter | `JIS_COVER_LETTER.docx`: addressed to Editor in Chief Sue McNeil (official JIS homepage, Wayback 2026-10-12), first-person singular, no desk-rejection history, no smart-grid framing, novelty not overstated | PASS (affiliation placeholder) |
| Charges | Conventional subscription route requested; no OA, no print colour, no excess-page charge selected | PASS |

## Conditions to clear before upload (author)

1. Enter author title, affiliation, postal address and corresponding email on the title page (`scripts/p32_manuscript_jis.py`, constants `AUTHOR`/`AFFIL`) and in the cover letter (`scripts/p36_cover_letter_jis.py`), then rebuild.
2. In Editorial Manager, re-confirm the current JIS editor, abstract/Practical Applications limits and APC/OA wording (the live ASCE pages could not be fetched from this environment; archived official copies were used).
3. Confirm that the public repository is synchronized to the PR commit (see handoff) so that the Data Availability Statement is accurate on the submission date.
4. Optional: mint a DOI for the repository snapshot (e.g., Zenodo) and update the `Onishi 2026` reference.

## Residual scientific risks (disclosed in the manuscript)

Reconstructed rather than observed networks; three purposive zones; economic Monte Carlo/tornado computed for the naive contrast, not for VoF; enumerated (not exhaustive) candidate set; no validation against utility decisions.
