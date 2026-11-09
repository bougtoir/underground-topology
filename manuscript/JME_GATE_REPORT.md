# Gated revision gate report — underground-topology → Journal of Management in Engineering (ASCE)
Branch: devin/1792362604-infra-renewal-retarget (based on devin/ceus-supplement-promote b991543, PR #689)
Date: 2026-10-18 UTC. Executed sequentially on one VM.

## GATE 0 — Inventory & freeze (PASS)
- Canonical manuscript: `manuscript/manuscript.docx` @ b991543 (PR #689, unmerged). 6 figures / 6 tables, no PV S3/Figure 7, no Supplement references (verified in document.xml).
- Frozen values verified against `analysis/manuscript_values_v3.csv` + `FINAL_V3_VALUE_CHECK.csv`: VoF 0.0145/0.3935/0.2010% (Sano/Kudamatsu/Yasu), 589 clusters / 554 feasible (360/88/106), 24 positive + 2 within numerical tolerance, zero mass 95.7%, 40-yr horizon, AC max|vm err| 0.0193 pu on 672 feeder–scenario objects, LV demand 58.6 MW, nodes 772/341/332.
- Equivalence margin: `config/ECONOMIC_EQUIVALENCE_SPEC.yaml` frozen pre-classification → "prespecified" is documented, retained.
- Public repo `github.com/bougtoir/underground-topology` reachable (default branch main).
- New finding: AC validation cohort = 672 feeder–scenario objects = 336 clusters × {S1,S2}, a subset (both-replicate-feasible) of the 554 feasible clusters. Previous wording "all feasible synthesized feeders" was ambiguous → corrected in text (see Gate 3).

## GATE 1 — Journal screen (PASS → JME)
Nonnegotiable filter: JCR JIF Q1 AND subscription route with zero mandatory author fees; no SAGE/MDPI/Hindawi.

| Journal | Publisher | Route | JIF (yr) | JCR Q | Mandatory fee | Verdict |
|---|---|---|---|---|---|---|
| **Journal of Management in Engineering** | ASCE | hybrid (OA opt. $2,750–3,000) | 7.0 (2024) | Q1 (Eng. Civil 13/183; Industrial 11/69, journal EOY review) | $0 | **TARGET** |
| Utilities Policy | Elsevier | hybrid (OA opt. $3,210) | ~4.4–4.9 | Q1 (claimed; verification weaker) | $0 | fallback #2 |
| Applied Energy | Elsevier | hybrid (OA opt. $4,210) | 11.0–12.2 | Q1 | $0 | #3 (scope stretch) |
| Energy Policy | Elsevier | hybrid (OA opt. $4,360) | 9.2–9.3 | Q1 | $0 | #4 |
| Reliability Eng. & System Safety | Elsevier | hybrid (OA opt. $4,830) | ~9 | Q1 | $0 | #5 (scope stretch) |
| Sustainable Cities and Society | Elsevier | hybrid (OA opt. $4,780) | ~11–13 | Q1 | $0 | #6 (CEUS-adjacent scope → desk-reject risk) |
| Int. J. Electrical Power & Energy Systems | Elsevier | **gold OA since 2024-01** | 5.0 | Q1 | **$4,190 mandatory → REJECT** | — |
| Structure and Infrastructure Eng. | T&F | subscription | 3.1 | **Q2 → REJECT** | $0 | — |
| J. Infrastructure Systems | ASCE | hybrid | 3.8 | **Q2 → REJECT** | $0 | — |
| Infrastructure Asset Management | ICE | — | ~no/low JIF | **not Q1 → REJECT** | — | — |

Fit scoring (0–5): JME 4.0 (renewal investment + asset management core scope), Utilities Policy 4.0, Applied Energy 3.0, Energy Policy 3.0, RESS 2.5, SCS 2.5. JME risks: 9% acceptance, scope requires asset-management framing (done in Gate 4). IEEE Trans. Power Systems excluded pre-emptively (mandatory overlength page charges beyond 8 pp).

Same-journal precedent added: Ochs et al. (2014, JME 30(1):41–49, doi:10.1061/(ASCE)ME.1943-5479.0000177) — infrastructure investment decisions via life-cycle cost. Verified via Crossref.

## GATE 2 — Adversarial review (no FATAL)
- MAJOR-1 CEUS-journal phrasing ("this journal's own literature", "CEUS's rehabilitation line") → fixed.
- MAJOR-2 AC validation cohort ambiguity (672 objects vs 554 feasible clusters) → fixed (336-cluster both-feasible subset stated).
- MAJOR-3 "best feasible redesign" optimality overclaim → qualified "within the enumerated candidate set".
- MINOR: morphology already demoted to exploratory diagnostic; zero-mass dominance stated. No new analyses warranted (Gate 3: verified reuse only).

## GATE 3 — Focused repair (PASS, text-only; no reruns)

## GATE 4–5 — Repositioning + citations (PASS)
- `manuscript/manuscript_jme.docx` (scripts/p21_manuscript_jme.py): abstract/keywords reframed to investment decision + asset management; intro adds Ochs et al.; discussion journal-agnostic; Data availability → bougtoir/underground-topology; orphan unreferenced media (old supplement DG figure) stripped.
- Citation ecology: 32 refs, all previously verified (`analysis/references_verified.csv`); only addition is Ochs et al. (Crossref-verified). Author-date style already matches ASCE.
- Figure caption order 1–6, table order 1–6 verified by body scan; all cited in text.

## GATE 6 — Data–text–figure QC (PASS)
- VoF/554/589/58.6MW/0.019pu match canonical CSVs. No hardcoded new result values introduced (p21 is a text-only patcher; numbers quoted verbatim from canonical docx).
- Render check: LibreOffice → 17-page PDF inspected (title page, Table 1, Figure 2 map, legible).

## GATE 7 — Finishing (PASS)
- `JME_submission_package_v1/`: manuscript.docx (JME version), cover_letter_jme.docx (first-person, asset-management framing), Figure_1..6.png, ZIP_MANIFEST_SHA256.txt; zip `JME_submission_package_v1.zip`.

## GATE 8 — Hostile review verdict: **SUBMIT-ready (pending user)**
Residual risks: (i) JME 9% acceptance — topically defensible but competitive; fallback = Utilities Policy. (ii) Author/affiliation placeholders remain (author task). (iii) 336/554 AC-validation cohort disclosed; reviewers may ask for full-cohort AC runs (linearized model already bounds error; feasible extension exists if requested). (iv) Public repo `bougtoir/underground-topology` must contain the reproduction code before submission — verify sync (BRANCH_MAP for this new branch required).

## Submission decision: proceed to PR; user approves before any submission.
