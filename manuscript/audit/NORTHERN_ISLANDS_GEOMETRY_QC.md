# Northern islands geometry QC
Defect: previous version drew a single coarse geoBoundaries RUS ADM0
administrative polygon (spanning 145.3-151.2E, low vertex resolution) —
blocky, inaccurate island outlines.
Fix: replaced ONLY the northern-island geometry with Natural Earth 10m
land polygons (public domain, ne_10m_land.zip, retrieved 2026-10-11,
EPSG:4326, persisted in data/raw/naturalearth/ne_10m_land/): per-island
components filtered by centroid in 143.4-150.5E / 43.0-46.4N — Habomai
group, Shikotan, Kunashir, Etorofu, Urup and adjacent islets. No
simplification; holes/rings preserved; no Sakhalin/mainland coastlines;
consistent fill/edge style with the Japan ADM1 coastline.
Unchanged: Japan ADM1 geometry, markers, legend, extent, panels b-d,
caption, all manuscript text/results.
