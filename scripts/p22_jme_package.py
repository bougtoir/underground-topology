"""Build JME cover letter docx + submission package zip."""
import docx, zipfile, hashlib, os, shutil

ROOT = __file__.rsplit("/scripts/", 1)[0]
PKG = f"{ROOT}/JME_submission_package_v1"
os.makedirs(PKG, exist_ok=True)

COVER = [
"Dear Dr. Cui,",
("I am submitting my manuscript, \"The Value of Topology Flexibility at Infrastructure Renewal: A "
"Feasibility-Gated Geospatial Assessment of Low-Voltage Re-Layout During Undergrounding,\" for consideration "
"in the Journal of Management in Engineering."),
("The paper asks a question that sits squarely in infrastructure asset management: when a municipality has "
"already committed to undergrounding an aging overhead distribution corridor, is it worth investigating a "
"re-layout of the low-voltage network at the same time, or is like-for-like replacement the defensible "
"default? I treat the renewal window as a bounded decision problem in which the incumbent layout remains an "
"admissible choice, and I price the option to re-draw the network rather than assuming it should be exercised."),
("Three contributions follow. First, I define a feasibility-gated, incumbent-admissible estimand — the value "
"of topology flexibility (VoF) — which removes the inflated savings that appear when the inherited layout is "
"excluded from the comparison set; a conventional incumbent-excluding contrast is shown to be artifact-prone. "
"Second, I provide an open-data reconstruction and engineering-gating pipeline spanning three municipal data "
"observability tiers, with every synthesized feeder checked by full AC power flow. Third, across 554 feasible "
"feeder clusters in three Japanese study zones, the option value is bounded (0.01–0.39% of like-for-like "
"life-cycle cost, inside a prespecified 1% practical-equivalence margin), zero for 96% of clusters, and "
"size-structured rather than morphology-driven — which converts a bounded, partly negative result into an "
"actionable screening rule for where detailed re-layout engineering is worth commissioning."),
("I am deliberately transparent that the magnitudes are modeled results conditional on reconstruction "
"assumptions, not observed utility savings. The transferable deliverable for asset managers and municipal "
"engineers is the screening method itself: a way to decide, before detailed design, whether a renewal corridor "
"merits a topology study at all. I believe this decision-framing and its disciplined treatment of a null "
"result are a natural fit for the journal's readership."),
("All code, the data-source registry, and machine-readable result tables are publicly available at "
"github.com/bougtoir/underground-topology. The manuscript is not under consideration elsewhere, and I declare "
"no conflict of interest. I would be glad to provide any further material the review requires."),
"Sincerely,",
"[Author name and affiliation — to be completed at submission]",
]

d = docx.Document()
st = d.styles['Normal']; st.font.name = 'Times New Roman'; st.font.size = docx.shared.Pt(11)
for t in COVER:
    d.add_paragraph(t)
d.save(f"{PKG}/cover_letter_jme.docx")

shutil.copy(f"{ROOT}/manuscript/manuscript_jme.docx", f"{PKG}/manuscript.docx")
FIGS = [
 ("figures/ceus_fig_pipeline.png","Figure_1.png"),
 ("figures/Figure2_preview.png","Figure_2.png"),
 ("figures/ceus_fig_routelength.png","Figure_3.png"),
 ("figures/v4_fig3_delta.png","Figure_4.png"),
 ("figures/ceus_fig_morphology.png","Figure_5.png"),
 ("figures/ceus_fig_decomposition.png","Figure_6.png"),
]
for src,dst in FIGS:
    shutil.copy(f"{ROOT}/{src}", f"{PKG}/{dst}")

zpath = f"{ROOT}/JME_submission_package_v1.zip"
if os.path.exists(zpath): os.remove(zpath)
sums=[]
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
    for f in sorted(os.listdir(PKG)):
        fp=f"{PKG}/{f}"
        z.write(fp, f)
        sums.append((f, hashlib.sha256(open(fp,'rb').read()).hexdigest()))
open(f"{PKG}/ZIP_MANIFEST_SHA256.txt","w").write("\n".join(f"{h}  {f}" for f,h in sums)+"\n")
print(os.listdir(PKG))
print(zpath)
