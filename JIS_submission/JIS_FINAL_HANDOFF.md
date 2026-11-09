# JIS Final Handoff

Date: 2026-11-09

## Decision
**CONDITIONAL SUBMIT** to ASCE *Journal of Infrastructure Systems* (Technical Paper). Conditions, all author actions: (1) enter title/affiliation/postal address/corresponding email in `scripts/p32_manuscript_jis.py` (`AUTHOR`, `AFFIL`) and `scripts/p36_cover_letter_jis.py`, then rebuild; (2) in Editorial Manager, re-confirm editor name, abstract/Practical Applications limits and OA/APC wording (live ASCE pages were blocked by HTTP 403; archived official copies used); (3) confirm public mirror is current. Not submitted. No OA, APC, page or colour charge selected (conventional route).

## Repository state
| Item | Value |
|---|---|
| Private repository | `bougtoir/wip`, subdirectory `underground_topology_segan/` |
| Source of truth (start) | `devin/ceus-supplement-promote` @ `d49bb52a2` (tree = `d5ce3a086`, PR #714 merged; identical to public main before this work) |
| Working branch | `devin/1794233571-jis-retarget` |
| Pull request | https://github.com/bougtoir/wip/pull/792 (base `devin/ceus-supplement-promote`) — **not merged** |
| Public mirror | https://github.com/bougtoir/underground-topology (journal-neutral name kept; no new repository). Synced through `devin/1790746503-segan-v4-review-fixes` (BRANCH_MAP/SUBDIR_MAP), which is advanced to the JIS commit with `data/raw/journal_jis/pages/` (archived ASCE page copies, ASCE copyright) removed from the public tree |
| Recommended merges | PR #792 after author review |
| Superseded | JME package (`manuscript/manuscript_jme.docx`, `scripts/p21_manuscript_jme.py`, `scripts/p22_jme_package.py`) is superseded for submission purposes but kept for provenance |

## Deliverables (`JIS_submission/`)
`JIS_MANUSCRIPT_FINAL.docx`, `JIS_MANUSCRIPT_FINAL.pdf`, `JIS_COVER_LETTER.docx`, `JIS_SUPPLEMENTAL_MATERIALS.docx`, `figures/Fig1–Fig5.tif`, `figures/FigS1.tif`, `figures/ALT_TEXT.txt`, `JIS_AUTHOR_GUIDELINES_AUDIT.md`, `JIS_SCOPE_AND_LITERATURE_FIT.md`, `JIS_SEMANTIC_CODE_AUDIT.md`, `JIS_REFERENCE_AUDIT.md`, `JIS_FIGURE_TABLE_CONSISTENCY.md`, `JIS_HOSTILE_REVIEW.md`, `JIS_FINAL_QC_REPORT.md`, this file, and `JIS_SUBMISSION_PACKAGE.zip` (all of the above + evidence CSVs + SHA256SUMS).

## Upload mapping for Editorial Manager
Manuscript: `JIS_MANUSCRIPT_FINAL.docx` · Figures: `Fig1.tif`–`Fig5.tif` (alt text from `ALT_TEXT.txt`) · Supplemental: `JIS_SUPPLEMENTAL_MATERIALS.docx` · Cover letter: `JIS_COVER_LETTER.docx`.

## Rebuild
```
cd underground_topology_segan
.venv/bin/python scripts/p31_ac_clusterload_check.py   # optional, ~2 min
.venv/bin/python scripts/p35_jis_figures.py
.venv/bin/python scripts/p32_manuscript_jis.py
(cd JIS_submission && soffice --headless --convert-to pdf JIS_MANUSCRIPT_FINAL.docx)
.venv/bin/python scripts/p36_cover_letter_jis.py
.venv/bin/python scripts/p34_reference_audit.py
.venv/bin/python scripts/p37_docx_qc_jis.py
.venv/bin/python scripts/p30_raw_ledger.py
.venv/bin/python scripts/p33_jis_package.py
.venv/bin/python -m unittest tests.test_vof_semantics tests.test_electrical_model
```
PDF rendering expects Times New Roman (`ttf-mscorefonts-installer`); without it LibreOffice substitutes Liberation Serif (metric-compatible).

## Key numbers (generated)
589 clusters (58.6 MW); 554 feasible (49.6 MW), 218 single-customer; VoF 0.01 / 0.39 / 0.20 % (Sano / Kudamatsu / Yasu), 24 positive clusters (max 6.1 %); 7 engineering variants 0.001–0.947 %; AC (cluster-terminal loading) 672/672 agreement, max |ΔV| 0.0056 pu.
