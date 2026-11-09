"""Build JIS_submission/JIS_COVER_LETTER.docx; numbers read from analysis outputs."""
import os, pandas as pd, docx
from docx.shared import Pt, RGBColor, Inches
from docx.oxml.ns import qn
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = f"{ROOT}/analysis"; Z = ["sano", "kudamatsu", "yasu"]
sr = pd.read_csv(f"{A}/scenario_results_v2.csv").set_index("city")
zm = pd.read_csv(f"{A}/CEUS_ZERO_MASS_SUMMARY.csv").set_index("city")
ac = pd.read_csv(f"{A}/JIS_AC_CLUSTERLOAD_CHECK.csv")
eng = pd.read_csv(f"{A}/ENGINEERING_ASSUMPTION_SENSITIVITY.csv")
N_all = int(sr.clusters.sum()); NF = int(sr.clusters_feasible.sum()); NPOS = int(zm.positive_vof.sum())
V = [f"{sr.loc[z,'vof_pct']:.2f}%" for z in Z]; VMAX = eng[eng.parameter != "baseline"].vof_pct.max()
TITLE = ("Is Network Reconfiguration Worth It at Infrastructure Renewal? A Feasibility-Gated Economic Screening "
         "of Low-Voltage Distribution Re-Layout during Undergrounding")
paras = [
 "November 9, 2026",
 "Professor Sue McNeil\nEditor in Chief, Journal of Infrastructure Systems\nAmerican Society of Civil Engineers",
 "Dear Professor McNeil,",
 f"I am pleased to submit the manuscript entitled \u201c{TITLE}\u201d for consideration as a Technical Paper in the "
 "Journal of Infrastructure Systems.",
 "The paper addresses a renewal decision that infrastructure managers face whenever buried networks are replaced. "
 "When a city converts overhead electricity distribution to underground cable, the excavation and duct works are "
 "committed and paid for, which creates a rare opportunity to change the layout of the low-voltage network at "
 "marginal cost. Whether that opportunity should be taken is usually assumed rather than evaluated.",
 "A technically feasible redesign is not automatically a worthwhile one. Network optimization studies typically "
 "compare an optimized layout with a greenfield or forced alternative, not with retention of the incumbent "
 "configuration, and the incumbent is often only partially recorded. I therefore formulate renewal as a choice in "
 "which like-for-like replacement remains admissible, and I define the value of reconfiguration as the expected "
 "life-cycle cost saving of the best redesign that passes explicit engineering feasibility gates (radiality, "
 "coincident-peak ampacity, transformer capacity, and voltage drop). Incumbent networks are reconstructed as "
 "ensembles from open municipal and OpenStreetMap data. The contribution is this decision estimand and screening "
 "procedure, not a new optimization algorithm; the non-negativity of the estimand follows from its formulation and "
 "is not presented as a finding.",
 f"In three Japanese study zones ({N_all} transformer-zone clusters, {NF} electrically feasible), the value of "
 f"reconfiguration was {V[0]}, {V[1]}, and {V[2]} of like-for-like life-cycle cost, all within a prespecified 1% "
 f"practical-equivalence margin and below {VMAX:.2f}% under every engineering-assumption variant. Value was positive "
 f"in only {NPOS} clusters, where it reached up to about 6%. Full AC power flow agreed with the linear feasibility "
 f"screen for all {len(ac)} feeder\u2013scenario cases. A conventional forced-redesign comparison instead reports a "
 "cost penalty of about 10% in one zone, which illustrates how excluding the incumbent can mislead.",
 "I believe this largely negative result is useful to the journal\u2019s readers because it supports like-for-like "
 "renewal as a defensible default for such networks and shows how a low-cost screening step can target detailed "
 "reconfiguration engineering to the few locations where it may pay. The work fits the journal\u2019s scope on "
 "sustaining and transforming civil infrastructure systems, including energy distribution, under uncertain "
 "information and with attention to economic flexibility. It builds on work published in the journal on valuing "
 "flexibility in utility network design (Basupi and Kapelan 2015), synthetic reconstruction of hidden utility "
 "networks (Fletcher et al. 2026), asset management under data scarcity (Dehghani et al. 2025), integrated "
 "planning of distribution networks (Kerwin and Adey 2021), and evaluation of underground renewal options "
 "(Hastak and Gokhale 2000).",
 "The conclusions are conditional on reconstructed rather than observed utility networks in three purposively "
 "selected zones, and the reported values are modeled screening estimates, not realized savings. The manuscript "
 "states these limitations and the evidence that would be needed before operational use.",
 "The manuscript is original, has not been published, and is not under consideration elsewhere. I am the sole "
 "author, I have no competing interests, and the work received no specific funding. All code, configuration, and "
 "generated results are publicly available, as described in the Data Availability Statement, and the use of AI "
 "tools is disclosed in the manuscript. The manuscript text and tables occupy 24 double-spaced pages and there are "
 "five figures, within the 30-page limit for Technical Papers. I request conventional (non-open-access) "
 "publication.",
 "Thank you for considering this submission.",
 "Sincerely,",
 "Tatsuki Onishi\n[Affiliation and postal address]\n[Email]",
]
d = docx.Document()
st = d.styles["Normal"]; st.font.name = "Times New Roman"; st.font.size = Pt(12); st.font.color.rgb = RGBColor(0, 0, 0)
rf = st.element.get_or_add_rPr().get_or_add_rFonts()
for a in list(rf.attrib): del rf.attrib[a]
for a in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"): rf.set(qn(a), "Times New Roman")
st.paragraph_format.space_after = Pt(10)
for s in d.sections:
    s.left_margin = s.right_margin = s.top_margin = s.bottom_margin = Inches(1)
for t in paras:
    p = d.add_paragraph()
    lines = t.split("\n")
    for i, ln in enumerate(lines):
        r = p.add_run(ln)
        if i < len(lines) - 1: r.add_break()
d.save(f"{ROOT}/JIS_submission/JIS_COVER_LETTER.docx")
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jis_docx_utils import sanitize_docx
sanitize_docx(f"{ROOT}/JIS_submission/JIS_COVER_LETTER.docx")
words = sum(len(t.split()) for t in paras)
assert " we " not in " ".join(paras).lower() and "desk" not in " ".join(paras).lower() and "smart grid" not in " ".join(paras).lower()
print("cover letter words", words)
