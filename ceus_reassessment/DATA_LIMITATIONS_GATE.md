# Gate 2 — data validity, spatial identification, reconstruction

Verified against files present in the repo (2026-10-10), not inferred.

## Sources & tiers (verified)

| Zone | Anchor evidence actually on disk | Tier interpretation |
|---|---|---|
| Sano | `data/raw/sano/sano_security_lights.csv` → `data/processed/sano_anchors.csv` with Japanese pole numbers (電柱番号), address, town-block name, management id, lat/lon | Tier-1 claim is grounded: anchors carry pole identifiers AND coordinates. Still security-light inventory, not a DSO pole/cable GIS — stated as anchors, never as actual cable routes. |
| Kudamatsu | `data/raw/kudamatsu/352071_security_lights*.csv` (3 shards; municipal open data, CC-BY) → geolocated anchors without pole linkage | Tier-2 verified. |
| Yasu | OSM roads (`osm_yasu.graphml`) + buildings (`osm_yasu_buildings.geojson`) only | Tier-3 verified; no anchor layer at all. |

License notes: municipal open data (Kudamatsu CC-BY per prior registry); OSM ODbL. Engineering sources persisted in `data/raw/engineering_sources/` (transformer catalogs, cable datasheets, statute, pandapower docs) — acquisition ledger exists in `provenance/`.

## Geometry / CRS

- `nodes.csv` per zone carries both lat/lon and projected `x_m`/`y_m`; all lengths in `edges.csv` are metres → no lat/lon-Euclidean distances used. PASS.
- Zone scale: ~740–830 road nodes, ~2000–2350 edges, 749–8126 buildings per zone (`zone_qc.json`). These are compact study zones extracted as the largest connected component — purposive, not city-wide, not a random sample of Japanese municipalities. Manuscript already frames selection as complementary data tiers, not representativeness.

## Boundary & snapping effects

- Mean building→road snap distance: Sano 41.1 m, Kudamatsu 49.1 m, Yasu 37.2 m. Demand snapping bias is acknowledged; feeder-route lengths inherit it.
- Edge truncation at zone boundary: clusters are formed within the extracted component; boundary feeders cannot route outside — a systematic containment effect, disclosed.
- OSM completeness not audited against national ground truth; stated as modeled demand surface, not measured.

## Spatial identification / pseudo-replication

- 3 zones ≠ 3 cities-sample-of-Japan; N feeder clusters are nested within zones → cluster-level statistics treated as *descriptive, spatially dependent* units. No cross-zone inferential tests, no p-values on zone contrasts. Any morphology→VoF relation reported descriptively with within-zone dependence flagged.
- MV-served exclusion (>150 kW) is a design assumption; LV modeled demand covers 74.7%/55.1%/53.4% of zone demand — reported, and contrasts cancel the excluded share.
- Reconstruction ensembles: 24-replicate + leave-one-family-out stability checked (S1 family NPC ratios ~1.00); anchor data feed reconstruction priors — validation is AC physics agreement on synthesized feeders, NOT incumbent-topology recovery. Stated.

## Verdict

PASS with transparent limitations — the urban-spatial interpretation is defensible as *descriptive, decision-support* analysis over three purposive zones. The estimand does not need redesigning; claims must stay bounded (planning-support, not measured utility performance).
