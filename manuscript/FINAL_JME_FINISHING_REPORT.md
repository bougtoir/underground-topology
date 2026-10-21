# FINAL JME FINISHING REPORT

Baseline: branch `devin/1792550201-jme-hostile-audit`, commits `af29d7c6a` (audit repairs) on top of merge `60025f678` (PR #708). Baseline artifact hashes preserved in `JME_submission_package_v1/ZIP_MANIFEST_SHA256.txt` (pre-finishing zip) and the Gate-0 audit report.

## Gate 0 — baseline: PASS
Canonical inputs: `JME_submission_package_v1/` (manuscript.docx sha 9497ea37…, cover_letter_jme.docx, Figures 1–6), `manuscript/FINAL_JME_HOSTILE_REPRO_AUDIT.md`. Data Availability URL in manuscript = https://github.com/bougtoir/underground-topology (correct, untouched).

## Gate 1 — cover letter AC denominator: PASS (fixed)
Paragraph 3 read "…with every synthesized feeder checked by full AC power flow." — false (AC validation covers a subset). Replaced with the prescribed wording: "with AC power-flow validation performed on 672 feeder–scenario objects across 336 clusters for which both incumbent and redesign scenarios were feasible." Manuscript already uses the correct subset wording — no change needed there. Letter re-rendered to PDF and visually inspected; first-person singular and style preserved.

## Gate 2 — AC-validation execution: PASS
The previously-running job (`scripts/p09_ac_validation.py` on clean public clone `/tmp/ut-pub`, pandapower 3.5.5, `AC_VS_LINEAR_VALIDATION.csv` written 2026-10-21 02:43 UTC; log `/tmp/p09.log`) **completed**. Output: "Feeders evaluated: 672 (0 non-converged) | |vm_ac − vm_lin| median 0.0001 pu, max 0.0193 pu (tol 0.02) | loss rel err median 0.003, max 0.226 (tol 0.25) | feasibility agreement 1.000 (tol 0.95) | AC vdrop max 11.36% vs linear 9.43%".
- Re-run CSV (673 rows incl. header = 672 objects, 336 clusters × {S1,S2}) vs committed canonical: all values identical except last-1–2-digit floating-point wobble in ~12 rows (e.g. 0.9938024462129447→…446; vm_abs_err changes <1e-9). Summary metrics identical to manuscript (max vm err 0.0193 pu). Classified: numerical nondeterminism, not a discrepancy — committed CSV retained, no reanalysis.

## Gate 3 — ZIP manifest: PASS (fixed)
Prior `ZIP_MANIFEST_SHA256.txt` listed itself (circular). Regenerated to cover exactly the 8 distributed artifacts (manuscript.docx, cover_letter_jme.docx, Figure_1–6.png), manifest excluded. Built `JME_submission_package_FINAL.zip`; extracted to a fresh dir and `sha256sum -c` → all 8 entries OK, no stale files.

## Gate 4 — targeted final QC: PASS
- Manuscript docx byte-identical to audited baseline (9497ea37…); 6 tables/6 figures present; no PV/Fig-7/S3 remnants; citation numbering coherent.
- Letter AC wording now matches manuscript Methods/Results (672 objects / 336-cluster subset vs 554-feasible primary cohort) and the actual AC log.
- Prior audits (hostile review, 29/29 DOI check, numeric reruns) remain valid — inputs unchanged.
- USER ACTION (not fabricated): `[Author name and affiliation — to be completed at submission]` placeholder retained in letter.
- Level-(iii) raw municipal/OSM rebuild still not claimed; published-code analytic reruns (p07b byte-identical, p04 benchmark, p11c freeze, p09 AC) are the demonstrated level.

## Files changed this pass
`JME_submission_package_v1/cover_letter_jme.docx` (AC sentence), `JME_submission_package_v1/ZIP_MANIFEST_SHA256.txt` (self-reference removed), `JME_submission_package_FINAL.zip` (new final archive). No manuscript, figure, or analysis changes.

## FINAL VERDICT: SUBMIT READY (subject to author metadata)
