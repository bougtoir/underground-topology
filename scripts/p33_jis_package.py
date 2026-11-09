"""Assemble the JIS submission package: separate figure files (TIFF, 300 dpi), alt text,
supplemental-materials file, and JIS_SUBMISSION_PACKAGE.zip containing the actual deliverables."""
import hashlib, os, shutil, zipfile
from PIL import Image
import docx
from docx.shared import Pt, Inches, RGBColor
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
J = f"{ROOT}/JIS_submission"; FO = f"{J}/figures"; os.makedirs(FO, exist_ok=True)
FIGS = [("ceus_fig_pipeline", "Fig1"), ("Figure2_preview", "Fig2"), ("jis_fig3_vof_zone", "Fig3"),
        ("jis_fig4_vof_distribution", "Fig4"), ("jis_fig5_decomposition", "Fig5"), ("ceus_fig_routelength", "FigS1")]
ALT = {
 "Fig1": "Flow diagram of six boxes: open urban data, demand model, reconstruction, feasibility gates, decision model, and outcome, connected by arrows.",
 "Fig2": "Map of Japan with markers for Sano, Kudamatsu, and Yasu, and three panels showing each study zone's road graph with building demand nodes.",
 "Fig3": "Bar chart by zone comparing the value of reconfiguration (0.01%, 0.39%, 0.20%) with the naive contrast, which is strongly negative in Kudamatsu; a gray band marks the plus or minus 1% margin.",
 "Fig4": "Left: bar chart of the share of feasible clusters with positive value by zone. Right: scatter of positive cluster values (log scale) against number of demand terminals.",
 "Fig5": "Three bar-chart panels, one per zone, decomposing the incumbent-minus-redesign cost difference into capital, loss, and other terms, plus the aggregate value of reconfiguration.",
 "FigS1": "Log-log scatter of redesign route length against incumbent route length for feasible clusters; most points lie on the identity line.",
}
for src, dst in FIGS:
    im = Image.open(f"{ROOT}/figures/{src}.png")
    if im.mode in ("RGBA", "P", "LA"):
        bg = Image.new("RGB", im.size, "white"); im = im.convert("RGBA"); bg.paste(im, mask=im.split()[-1]); im = bg
    im.save(f"{FO}/{dst}.tif", dpi=(300, 300), compression="tiff_lzw")
with open(f"{FO}/ALT_TEXT.txt", "w") as fh:
    for k, v in ALT.items(): fh.write(f"{k}: {v}\n")
# supplemental materials
d = docx.Document(); st = d.styles["Normal"]; st.font.name = "Times New Roman"; st.font.size = Pt(12); st.font.color.rgb = RGBColor(0, 0, 0)
d.add_paragraph().add_run("Supplemental Materials").bold = True
d.add_paragraph("Is Network Reconfiguration Worth It at Infrastructure Renewal? A Feasibility-Gated Economic "
                "Screening of Low-Voltage Distribution Re-Layout during Undergrounding")
d.add_picture(f"{ROOT}/figures/ceus_fig_routelength.png", width=Inches(5.5))
d.add_paragraph("Fig. S1. Route length of the least-cost feasible redesign versus the reconstructed incumbent for "
                "all feasible clusters (log–log axes).")
d.save(f"{J}/JIS_SUPPLEMENTAL_MATERIALS.docx")
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jis_docx_utils import sanitize_docx; sanitize_docx(f"{J}/JIS_SUPPLEMENTAL_MATERIALS.docx")
# zip
DOCS = ["JIS_MANUSCRIPT_FINAL.docx", "JIS_MANUSCRIPT_FINAL.pdf", "JIS_COVER_LETTER.docx", "JIS_SUPPLEMENTAL_MATERIALS.docx",
        "JIS_AUTHOR_GUIDELINES_AUDIT.md", "JIS_SCOPE_AND_LITERATURE_FIT.md", "JIS_SEMANTIC_CODE_AUDIT.md",
        "JIS_REFERENCE_AUDIT.md", "JIS_FIGURE_TABLE_CONSISTENCY.md", "JIS_HOSTILE_REVIEW.md", "JIS_FINAL_QC_REPORT.md",
        "JIS_FINAL_HANDOFF.md"]
EVID = ["analysis/scenario_results_v2.csv", "analysis/CEUS_ZERO_MASS_SUMMARY.csv", "analysis/AC_VS_LINEAR_VALIDATION.csv",
        "analysis/JIS_AC_CLUSTERLOAD_CHECK.csv", "analysis/JIS_AC_CLUSTERLOAD_REPORT.md",
        "analysis/ENGINEERING_ASSUMPTION_SENSITIVITY.csv", "analysis/MORPHOLOGY_CORRELATIONS_CORRECTED.csv",
        "analysis/CEUS_SPATIAL_DIAGNOSTICS.csv", "analysis/sensitivity_mc_v2.csv", "analysis/JIS_REFERENCE_CHECK.csv",
        "analysis/JIS_DOCX_QC.json", "data/raw/journal_jis/RETRIEVAL_LEDGER.csv"]
missing = [x for x in DOCS if not os.path.exists(f"{J}/{x}")] + [x for x in EVID if not os.path.exists(f"{ROOT}/{x}")]
manifest = []
zp = f"{J}/JIS_SUBMISSION_PACKAGE.zip"
with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
    for x in DOCS:
        if os.path.exists(f"{J}/{x}"): z.write(f"{J}/{x}", f"JIS_SUBMISSION_PACKAGE/{x}"); manifest.append(f"{J}/{x}")
    for f in sorted(os.listdir(FO)):
        z.write(f"{FO}/{f}", f"JIS_SUBMISSION_PACKAGE/figures/{f}"); manifest.append(f"{FO}/{f}")
    for x in EVID:
        if os.path.exists(f"{ROOT}/{x}"): z.write(f"{ROOT}/{x}", f"JIS_SUBMISSION_PACKAGE/evidence/{x}"); manifest.append(f"{ROOT}/{x}")
    lines = [f"{hashlib.sha256(open(p,'rb').read()).hexdigest()}  {os.path.relpath(p, ROOT)}" for p in manifest]
    z.writestr("JIS_SUBMISSION_PACKAGE/SHA256SUMS.txt", "\n".join(lines) + "\n")
print("zip:", zp, len(manifest), "files; missing:", missing)
