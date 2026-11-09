"""Shared DOCX post-processing for JIS deliverables: force black text and Times New Roman in all style definitions."""
import re, shutil, zipfile, os

def sanitize_docx(path):
    tmp = path + ".tmp"
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename in ("word/styles.xml", "word/document.xml", "word/footer1.xml"):
                s = data.decode("utf-8")
                s = re.sub(r'<w:color [^>]*/>', '<w:color w:val="000000"/>', s)
                s = re.sub(r'w:(ascii|hAnsi|eastAsia|cs)="(?!Cambria Math)[^"]+"', r'w:\1="Times New Roman"', s)
                s = re.sub(r' w:(ascii|hAnsi|eastAsia|cs)Theme="[^"]+"', "", s)
                data = s.encode("utf-8")
            zout.writestr(item, data)
    shutil.move(tmp, path)
