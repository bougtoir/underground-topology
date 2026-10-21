"""Build manuscript_jme.docx from manuscript.docx (canonical, 6 figs / 6 tables).

Journal of Management in Engineering (ASCE) retarget edits only:
- remove CEUS-journal phrasing ("this journal", "CEUS's ...")
- add engineering-management framing + Ochs et al. (2014, JME) citation
- clarify AC-validation cohort (672 feeder-scenario objects / 336 clusters)
- qualify "best" as within the enumerated candidate set
- update public repository name to bougtoir/underground-topology
All numeric claims are unchanged; canonical values stay in analysis/ CSVs.
"""
import shutil, docx

ROOT = __file__.rsplit("/scripts/", 1)[0]
SRC = f"{ROOT}/manuscript/manuscript.docx"
DST = f"{ROOT}/manuscript/manuscript_jme.docx"

ABSTRACT = ("Urban renewal programs that replace aging overhead distribution lines with underground cables "
"face a rarely asked investment question: when the corridor is already committed, is re-drawing the local "
"network worth anything? This study quantifies the value of topology flexibility (VoF) at renewal as an "
"infrastructure investment decision problem. Legacy low-voltage networks are reconstructed from open municipal "
"and OpenStreetMap data in three Japanese study zones spanning three observability tiers; candidate re-layouts "
"are synthesized as weighted Steiner trees on the road graph under explicit engineering feasibility gates "
"(coincident-load sizing, ampacity, ~150 kVA transformer zones, 6% voltage-drop limit) with AC power-flow "
"validation on the synthesized feasible feeders. Across 554 feasible feeder clusters serving 58.6 MW of modeled "
"demand, VoF is 0.01%, 0.39%, and 0.20% of like-for-like life-cycle cost — inside a prespecified 1% "
"practical-equivalence margin. Residual flexibility value is rare and spatially concentrated: 96% of feasible "
"clusters show zero value, and apparent morphology correlates do not survive adjustment for cluster size. "
"Like-for-like renewal is a defensible default at this scale; the transferable contribution is a screening "
"method that tells asset managers where re-layout assessment is worth its engineering cost, not the magnitudes "
"themselves.")

KEYWORDS = ("Keywords: infrastructure renewal; asset management; undergrounding; life-cycle cost; "
"network reconstruction; Steiner tree; investment decision")

INTRO_TAIL_OLD = ("Within this journal's own literature, decision-support for buried-utility rehabilitation is an "
"established theme (Hadzilacos et al., 2000), network geometry has been inferred from incomplete surface "
"evidence (Chahinian et al., 2019), and geospatial integration methods tolerate partial utility semantics "
"(Gilbert et al., 2021).")
INTRO_TAIL_NEW = ("Decision support for buried-utility rehabilitation is an established theme "
"(Hadzilacos et al., 2000), network geometry has been inferred from incomplete surface evidence "
"(Chahinian et al., 2019), and geospatial integration methods tolerate partial utility semantics "
"(Gilbert et al., 2021). In the engineering-management literature, renewal is formalized as a life-cycle "
"replacement problem (Ochs et al., 2014), yet the renewal window is rarely treated as a spatial design choice.")

ELEC_OLD = ("The linearized branch-flow model (Gan and Low, 2014) was validated against pandapower AC power flow "
"(Thurner et al., 2018) on all feasible synthesized feeders;")
ELEC_NEW = ("The linearized branch-flow model (Gan and Low, 2014) was validated against pandapower AC power flow "
"(Thurner et al., 2018) on the synthesized feasible feeders — 672 feeder–scenario objects spanning the 336 "
"clusters in which both the incumbent and a feasible redesign replicate exist;")

ENUM_OLD = ("Candidate sets are enumerated per feeder cluster; the incumbent-like replicate remains in the "
"admissible set.")
ENUM_NEW = ("Candidate sets are enumerated per feeder cluster; the incumbent-like replicate remains in the "
"admissible set, and 'best' is always taken within the enumerated candidate set, not over the untried "
"re-layout space.")

RES_OLD = ("AC validation on all feasible synthesized feeders gives max voltage-magnitude deviation 0.019 pu "
"against a 0.02 tolerance and feasibility agreement 1.00 over 672 feeders.")
RES_NEW = ("AC validation on the 672 feeder–scenario objects spanning 336 clusters with both feasible replicates "
"gives max voltage-magnitude deviation 0.019 pu against a 0.02 tolerance and feasibility agreement 1.00.")

DISC_OLD = "Relative to CEUS's rehabilitation decision-support line"
DISC_NEW = "Relative to rehabilitation decision-support systems"
DISC2_OLD = "And relative to proxy-location network inference in this journal"
DISC2_NEW = "And relative to proxy-location network inference"

DATA_OLD = "github.com/bougtoir/underground-topology-segan"
DATA_NEW = "github.com/bougtoir/underground-topology"

OCHS_REF = ("Ochs, K.S., Miller, M.E., Thal, A.E. and Ritschel, J.D. (2014). Proposed method for analyzing "
"infrastructure investment decisions involving rapidly evolving technology: case study of LED streetlights. "
"Journal of Management in Engineering 30(1): 41–49. doi:10.1061/(ASCE)ME.1943-5479.0000177")

d = docx.Document(SRC)
edits = 0

def replace_in_para(p, old, new):
    global edits
    if old not in p.text:
        return False
    # rebuild paragraph text with replacement, preserving first run's formatting
    text = p.text.replace(old, new)
    if not p.runs:
        return False
    p.runs[0].text = text
    for r in p.runs[1:]:
        r.text = ""
    edits += 1
    return True

for i, p in enumerate(d.paragraphs):
    t = p.text
    if i == 3 and t.startswith("Urban renewal programs"):
        p.runs[0].text = ABSTRACT
        for r in p.runs[1:]: r.text = ""
        edits += 1
    elif i == 4 and t.startswith("Keywords:"):
        p.runs[0].text = KEYWORDS
        for r in p.runs[1:]: r.text = ""
        edits += 1
    elif "Within this journal's own literature" in t:
        replace_in_para(p, INTRO_TAIL_OLD, INTRO_TAIL_NEW)
    elif "on all feasible synthesized feeders" in t and "Gan and Low" in t:
        replace_in_para(p, ELEC_OLD, ELEC_NEW)
    elif "Candidate sets are enumerated per feeder cluster" in t:
        replace_in_para(p, ENUM_OLD, ENUM_NEW)
    elif "AC validation on all feasible synthesized feeders" in t:
        replace_in_para(p, RES_OLD, RES_NEW)
    elif "CEUS's rehabilitation" in t:
        replace_in_para(p, DISC_OLD, DISC_NEW)
        p2 = d.paragraphs[i]  # same object
        replace_in_para(p2, DISC2_OLD, DISC2_NEW)
    elif "underground-topology-segan" in t:
        replace_in_para(p, DATA_OLD, DATA_NEW)
    elif "Louf, R. and Barthélemy, M." in t:
        # insert Ochs reference after Louf (alphabetical: Louf < Ochs < Samui... wait: 'Sano' follows Louf? order is ... Levinson, Liu, Louf, Sano → Ochs between Louf and Sano)
        newp = p._p.addnext(p._p.__class__())
        pass

# insert Ochs reference: find Louf ref paragraph, clone-insert after it
from copy import deepcopy
for i, p in enumerate(d.paragraphs):
    if p.text.startswith("Louf, R. and Barthélemy"):
        new_el = deepcopy(p._p)
        p._p.addnext(new_el)
        np = d.paragraphs[i+1]
        np.runs[0].text = OCHS_REF
        for r in np.runs[1:]: r.text = ""
        edits += 1
        break

print("edits:", edits)
d.save(DST)

# verify
d2 = docx.Document(DST)
full = "\n".join(pp.text for pp in d2.paragraphs)
for bad in ["this journal", "CEUS", "segan", "S3", "photovoltaic", "Supplement"]:
    hits = [l for l in full.split("\n") if bad in l]
    print(bad, len(hits))
print("Ochs present:", "Ochs" in full)
