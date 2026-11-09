"""Write a machine-readable retrieval ledger for data/raw/journal_jis (SHA-256, size, source)."""
import csv, hashlib, os, re, datetime
ROOT = __file__.rsplit("/scripts/", 1)[0]
RAW = f"{ROOT}/data/raw/journal_jis"
OUT = f"{RAW}/RETRIEVAL_LEDGER.csv"
WB = {
 "jis_home_wb20261012": "http://web.archive.org/web/20261012201643id_/https://ascelibrary.org/journal/jitse4",
 "jis_editorial_board_wb20240608": "http://web.archive.org/web/20240608194818id_/https://ascelibrary.org/page/jitse4/editorialboard",
 "asce_author_center_journal_wb20231204": "http://web.archive.org/web/20231204120220id_/https://ascelibrary.org/author-center/journal",
 "asce_author_center_journal_wb20240924": "http://web.archive.org/web/20240924145901id_/https://ascelibrary.org/author-center/journal?cookieSet=1",
 "asce_ai_policy_wb20261002": "http://web.archive.org/web/20261002213154id_/https://ascelibrary.org/author-center/ai-policy",
 "asce_data_availability_wb20240607": "http://web.archive.org/web/20240607225713id_/https://ascelibrary.org/author-center/data-availability",
 "asce_preparing_manuscript_wb20260416": "http://web.archive.org/web/20260416233657id_/https://ascelibrary.org/author-center/preparing-manuscript",
 "asce_author_center_wb20250727": "http://web.archive.org/web/20250727175414id_/https://ascelibrary.org/author-center?cookieSet=1",
 "asce_rights_permissions_wb20240717": "http://web.archive.org/web/20240717202942id_/https://ascelibrary.org/author-center/rights-permissions?cookieSet=1",
}
def source(rel):
    base = os.path.basename(rel); stem = re.sub(r"(_decoded)?\.(html\.raw|html|txt)$", "", base)
    if rel.startswith("crossref_works/"): return "https://api.crossref.org/works/<DOI>", "Crossref REST API single-work record", "Crossref metadata: CC0"
    if rel.startswith("crossref/"): return "https://api.crossref.org/journals/1943-555X/works?query.bibliographic=<q>&rows=40", "Crossref journal search, first page only (rows=40); not exhaustive", "Crossref metadata: CC0"
    if rel.startswith("openalex/"): return "https://api.openalex.org/works/https://doi.org/<DOI>", "OpenAlex single-work record (abstract inverted index)", "OpenAlex: CC0"
    if stem in WB: return WB[stem], "Internet Archive Wayback snapshot of official ASCE page (live page HTTP 403 bot check)", "ASCE copyright; archived copy kept for audit only"
    if rel.startswith("pages/"): return "https://ascelibrary.org (live, via Chrome CDP)", "Live fetch returned HTTP 403 Cloudflare bot-check page (evidence of inaccessibility)", "ASCE copyright"
    return "", "derived/aggregate", ""
rows = []
for dp, _, fs in os.walk(RAW):
    for f in sorted(fs):
        p = os.path.join(dp, f); rel = os.path.relpath(p, RAW)
        if rel == "RETRIEVAL_LEDGER.csv": continue
        b = open(p, "rb").read(); url, cond, terms = source(rel)
        mt = datetime.datetime.fromtimestamp(os.path.getmtime(p), datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        rows.append([rel, url, cond, mt, len(b), hashlib.sha256(b).hexdigest(), terms])
with open(OUT, "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["path", "source_url", "conditions", "retrieved_utc_file_mtime", "bytes", "sha256", "usage_terms"]); w.writerows(sorted(rows))
print(len(rows), "files ->", OUT)
