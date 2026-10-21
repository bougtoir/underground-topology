# INLINE FIGURE ORDER FINAL AUDIT — GO
Method: reopened manuscript_inline_ceus_final.docx from disk; traversed
word/document.xml body in order, pairing each a:blip drawing (rId->
media part) with the next "Figure N." caption paragraph.
Results:
- Embedded image document-order: pos 10,15,30,32,35,37 ->
  media/image1,image2,image4,image3,image6,image5.png
- Paired captions: 1,2,3,4,5,6 — EXACT order asserted.
- Note: media part FILENAMES are numbered by python-docx insertion
  call order (image4.png=Figure 3 etc.). Part names are arbitrary;
  authoritative order is body XML position, which is correct. A check
  that sorts by media filename (1,2,4,3,6,5) would report a false
  failure; document traversal is the correct criterion.
- Image bytes: all 6 embedded PNGs SHA-256 == figures/ source PNGs
  (Fig2 = approved map, byte-identical).
- First in-text citation order: 1->6 asserted.
- Prose: canonical text is exact ordered subsequence of inline text
  (excluding figure captions) — no prose changes.
- Exactly one image+caption unit per figure; end "Figure captions"
  list is the separate-figure submission caption list, distinct from
  embedded units.
