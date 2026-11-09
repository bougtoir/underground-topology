"""Verify every DOI in the JIS manuscript reference list against Crossref.
Raw Crossref JSON is stored under data/raw/journal_jis/crossref_works/ (existing files are never overwritten).
Writes analysis/JIS_REFERENCE_CHECK.csv."""
import csv, json, os, re, time, urllib.request, urllib.parse, unicodedata
import docx
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = f"{ROOT}/data/raw/journal_jis/crossref_works"; os.makedirs(RAW, exist_ok=True)
d = docx.Document(f"{ROOT}/JIS_submission/JIS_MANUSCRIPT_FINAL.docx")
paras = [p.text for p in d.paragraphs]
i0 = paras.index("References"); i1 = paras.index("Figure Captions")
refs = [t for t in paras[i0 + 1:i1] if t.strip()]
def norm(s): return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKD", s.lower()))
rows = []
for r in refs:
    m = re.search(r"https://doi\.org/(\S+?)\.?$", r)
    if not m:
        rows.append(dict(reference=r[:80], doi="", status="NO-DOI (web/data source)")); continue
    doi = m.group(1)
    fn = f"{RAW}/{re.sub(r'[^A-Za-z0-9._-]', '_', doi)}.json"
    if not os.path.exists(fn):
        url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="")
        req = urllib.request.Request(url, headers={"User-Agent": "jis-ref-audit (mailto:bougtoir@gmail.com)"})
        open(fn, "wb").write(urllib.request.urlopen(req, timeout=30).read()); time.sleep(0.3)
    w = json.load(open(fn))["message"]
    title = (w.get("title") or [""])[0]
    yr = (w.get("published-print") or w.get("published-online") or w.get("issued"))["date-parts"][0][0]
    yrs = {str(x["date-parts"][0][0]) for k in ("published-print", "published-online", "issued") if (x := w.get(k))}
    vol, iss, pg = w.get("volume", ""), w.get("issue", ""), w.get("page", w.get("article-number", ""))
    fam = (w.get("author") or [{}])[0].get("family", "")
    ry = re.search(r"\. (\d{4}|n\.d\.)\. ", r).group(1)
    chk = dict(title=norm(title)[:40] in norm(r), year=ry in yrs, volume=(not vol) or f" {vol} " in r or f" {vol}:" in r,
               issue=(not iss) or f"({iss})" in r.replace(" (", "("),
               page=(not pg) or pg.replace("-", "–") in r or pg in r, author=norm(fam) in norm(r[:60]))
    rows.append(dict(reference=r[:80], doi=doi, cr_title=title[:90], cr_year=yr, cr_years="/".join(sorted(yrs)),
                     cr_volume=vol, cr_issue=iss, cr_page=pg, cr_first_author=fam,
                     container=(w.get("container-title") or [""])[0][:60],
                     status="OK" if all(chk.values()) else "CHECK: " + ",".join(k for k, v in chk.items() if not v)))
with open(f"{ROOT}/analysis/JIS_REFERENCE_CHECK.csv", "w", newline="") as fh:
    wr = csv.DictWriter(fh, fieldnames=sorted({k for r in rows for k in r}, key=lambda k: list(rows[1]).index(k) if k in rows[1] else 99))
    wr.writeheader(); wr.writerows(rows)
for r in rows:
    if r["status"] != "OK": print(r["status"], "|", r["reference"][:60], "|", r.get("cr_title", "")[:50], r.get("cr_years", ""), r.get("cr_volume", ""), r.get("cr_issue", ""), r.get("cr_page", ""))
print(len(rows), "refs;", sum(r["status"] == "OK" for r in rows), "OK")
