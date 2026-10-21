# Figure 2 map provenance (current)
- Japan prefecture polygons: geoBoundaries JPN ADM1 (CC-BY-4.0, William &
  Mary geoLab, https://www.geoboundaries.org/, releaseData commit
  9469f09), raw data/raw/geoboundaries/geoBoundaries-JPN-ADM1.geojson
  (SHA-256 fc30ddd3..., retrieved 2026-10-11 UTC).
- Northern-island coastlines: Natural Earth 10m land, ne_10m_land.zip
  (public domain, https://www.naturalearthdata.com/), raw
  data/raw/naturalearth/ne_10m_land/ (retrieved 2026-10-11); island
  polygons selected by centroid 143.4-150.5E / 43.0-46.4N.
- geoBoundaries RUS ADM0 was downloaded but is NOT rendered in the
  final figure (superseded by Natural Earth coastlines).
- CRS EPSG:4326, aspect corrected at 36 deg N; script
  scripts/p20_geographic_context_fig.py; municipal markers from
  zone.geojson centroids; legend lists Sano / Kudamatsu / Yasu.
