"""Automated DOCX/PDF QC for the JIS manuscript and cover letter -> analysis/JIS_DOCX_QC.json"""
import json, os, re, subprocess, zipfile
import docx
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
J = f"{ROOT}/JIS_submission"; W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
res = {}
def chk(name, ok, detail=""):
    res[name] = {"pass": bool(ok), "detail": detail}
for fn in ("JIS_MANUSCRIPT_FINAL.docx", "JIS_COVER_LETTER.docx"):
    z = zipfile.ZipFile(f"{J}/{fn}"); xml = z.read("word/document.xml").decode()
    sty = z.read("word/styles.xml").decode()
    fonts = set(re.findall(r'w:ascii="([^"]+)"', xml + sty)) - {"Cambria Math"}
    chk(f"{fn}: fonts Times New Roman only (Cambria Math in OMML)", fonts <= {"Times New Roman"}, sorted(fonts))
    cols = set(re.findall(r'<w:color w:val="([0-9A-Fa-f]{6}|auto)"', xml + sty))
    chk(f"{fn}: text color black/auto", cols <= {"000000", "auto"}, sorted(cols))
    chk(f"{fn}: no character spacing", not re.search(r"<w:rPr>(?:(?!</w:rPr>).)*<w:spacing ", xml), "")
    chk(f"{fn}: no embedded images", "<w:drawing" not in xml and not any(n.startswith("word/media") for n in z.namelist()), "")
    chk(f"{fn}: no attached template (.dot/.dotx)", "attachedTemplate" not in z.read("word/settings.xml").decode(), "")
    d = docx.Document(f"{J}/{fn}")
    chk(f"{fn}: no hard line breaks inside body paragraphs", not any("\n" in p.text for p in d.paragraphs if len(p.text) > 200), "")
m = docx.Document(f"{J}/JIS_MANUSCRIPT_FINAL.docx")
xml = zipfile.ZipFile(f"{J}/JIS_MANUSCRIPT_FINAL.docx").read("word/document.xml").decode()
chk("native OMML equations (3)", xml.count("<m:oMath") == 3 and xml.count("<m:oMath>") + xml.count("<m:oMath ") == 3, xml.count("<m:oMath"))
heads = [p.text for p in m.paragraphs if p.style.name.startswith("Heading")]
chk("headings unnumbered", not any(re.match(r"^\d", h) for h in heads), "")
order = ["Abstract", "Practical Applications", "Introduction", "Methods", "Results", "Discussion", "Conclusions",
         "Data Availability Statement", "Acknowledgments", "Disclosure of AI Tool Use", "Supplemental Materials",
         "References", "Figure Captions"]
pos = [heads.index(h) if h in heads else -1 for h in order]
chk("ASCE section order", all(p >= 0 for p in pos) and pos == sorted(pos), dict(zip(order, pos)))
txt = [p.text for p in m.paragraphs]
i = txt.index("Abstract"); ab = txt[i + 1]; pa = txt[txt.index("Practical Applications") + 1]
chk("abstract 250-300 words, no citations/equations", 250 <= len(ab.split()) <= 300 and not re.search(r"\(\w[^()]*\d{4}\)", ab), len(ab.split()))
chk("practical applications 150-200 words", 150 <= len(pa.split()) <= 200, len(pa.split()))
body = " ".join(txt[txt.index("Introduction"):txt.index("References")])
figs = [int(x) for x in re.findall(r"Fig\. (\d)", body)]; tabs = [int(x) for x in re.findall(r"Table (\d)", body)]
first = lambda seq: [x for k, x in enumerate(seq) if x not in seq[:k]]
chk("figures cited sequentially", first(figs) == sorted(set(figs)) == list(range(1, max(figs) + 1)), first(figs))
chk("tables cited sequentially", first(tabs) == sorted(set(tabs)) == list(range(1, max(tabs) + 1)), first(tabs))
chk("no 'Figure n' in-text style (ASCE uses Fig.)", not re.search(r"\bFigure \d", body), "")
caps = txt[txt.index("Figure Captions") + 1:]
chk("captions begin 'Fig.'", all(c.startswith("Fig. ") for c in caps if c.startswith("Fig")), "")
chk("no stale journal names", not re.search(r"\b(CEUS|JME|SEGAN|CAIE|Computers, Environment and Urban Systems|Journal of Management in Engineering)\b", body), "")
chk("Data Availability Statement uses ASCE verbatim option", "are available in a repository online in accordance with funder data retention policies." in body, "")
pdf = f"{J}/JIS_MANUSCRIPT_FINAL.pdf"
pages = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout).group(1))
nfig = len([c for c in caps if re.match(r"Fig\. \d", c)])
chk("length <= 30 pages incl. figures (1 page per figure)", pages + nfig <= 30, f"{pages} text/table pages + {nfig} figures = {pages + nfig}")
fontsout = subprocess.run(["pdffonts", pdf], capture_output=True, text=True).stdout
chk("PDF fonts embedded", all(l.split()[-5] == "yes" for l in fontsout.splitlines()[2:] if l.strip()), "")
json.dump(res, open(f"{ROOT}/analysis/JIS_DOCX_QC.json", "w"), indent=1, ensure_ascii=False)
for k, v in res.items(): print("PASS" if v["pass"] else "FAIL", k, v["detail"] if not v["pass"] else "")
