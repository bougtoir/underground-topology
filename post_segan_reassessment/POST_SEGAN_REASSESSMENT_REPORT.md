# POST-SEGAN REASSESSMENT REPORT

## Editorial decision, read precisely

SEGAN-D-26-05388 desk rejection (EiC Gianfranco Chicco): "many of the discussions are in the
domain of layout of network and application of smart grid network is limited. In fact there
is no discussion on proposed study on direct performance/operation of smart grid
application." This is a *scope-fit* judgment: the paper is a network-layout / planning study,
not a smart-grid operations study. It is **not** a peer validation or invalidation of the
methods — no reviewer reached the technical content.

## Scientific value (after Phase 1 audit)

- Strongest claims: (a) the nonnegative VoF estimand — redesign as an *option* with the
  incumbent admissible — exposing that headline forced-redesign savings are estimand
  artifacts; (b) feasibility-first audit showing physics gating removes fictitious
  headroom; (c) reconstruction-ensemble uncertainty propagation; (d) a bounded, honest
  answer: VoF 0.01–0.39% of NPC, inside the prespecified 1% margin.
- Weakest claims: reconstructed (unobserved) topologies; modeled demand; three Japanese
  zones; surrogate AC-validated on synthesized feeders only; the 1% margin is a
  model-resolution rule, not a statistical equivalence test.
- Contribution type: applied infrastructure planning / decision analysis — not a new
  algorithm and not smart-grid operation.

## Closest prior work (Phase 2)

Full matrix in 02_CLOSEST_PRIOR_WORK_MATRIX.csv (16 rows). No prior work was found that
estimates the option value of topology redesign at the renewal window with incumbent
admissible in the choice set, feasibility gating, and reconstruction-ensemble uncertainty.
Closest neighbors: undergrounding CBA (Larsen 2016; Fenrick & Getachew 2012 — system-level
policy evaluation, not design-space choice), feeder routing (Samui 2012; Kumar 2014 —
greenfield/expansion, no incumbent-preserving contrast), synthetic LV topology generation
(Abhilash/Bandam et al. 2021; synthetic grid generator 2024 — topology synthesis without
economic option evaluation). Novelty verdict: real but bounded increment — a
measurement/estimand contribution, not a methods theorem.

## Disciplinary reframing (Phase 3)

| Framing | Substantiable without new experiments? | Venue fit |
|---|---|---|
| Distribution expansion/renewal planning | Yes — but natural venues gated (IJEPES gold-OA, EPSR/TPWRD Q2, TPWRS overlength) | Partial — TPWRS conditional only |
| Infrastructure asset management / whole-life investment | Yes — VoF, feasibility gating, life-cycle NPC are already the paper's spine | Strong — CAIE, RESS, JME, SEPS |
| Infrastructure layout / civil systems optimization | Yes — road-graph Steiner synthesis | Moderate — TUST, CEUS |
| Applied energy economics / investment decision | Weak — not an econometric/policy paper | Weak |

## Journal selection (Phases 4–5)

16 candidates fully audited, 14 ELIGIBLE at zero mandatory cost on the subscription route
(hard gates: JCR-2024 JIF Q1 + total mandatory author charges = 0). Excluded: IJEPES (gold
OA, $4,190), Energy Economics ($100 submission fee), EPSR/TPWRD/Utilities Policy/SETA/JIS
(JCR Q2), TSG (scope mismatch + overlength), OA titles (IET GTD, ITEES, MPCE, CSEE JPES,
Energies…). IEEE TPWRS kept conditional (mandatory $250/page beyond 12pp).

## Recommendation (Phase 6 gate)

**A — REPOSITION NOW.** Primary target: **Computer-Aided Civil and Infrastructure
Engineering** (Wiley; JIF 9.1, JCR Q1 in Engineering, Civil & two more categories; hybrid —
traditional subscription route carries no APC, no submission fee, no page charges). The
paper's spine (computational infrastructure network planning + life-cycle decision analysis
on real municipal geographies) fits CAIE's scope better than any power venue left open.
Alternates: Reliability Engineering & System Safety; Socio-Economic Planning Sciences;
Computers & Industrial Engineering; Tunnelling & Underground Space Technology.

Adaptation executed in `scripts/p13e_manuscript_caie.py`: reframe Introduction/Discussion
toward infrastructure renewal planning and decision-analysis contributions; author-date
citations; five material references added; "pre-registered"→"prespecified"; SEGAN-specific
framing removed. No new simulations; frozen values intact.
