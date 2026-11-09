# Results change log (reanalysis vs v1)
1. Horizon prose: "30-year discounted losses" -> "40-year discounted losses"
   (primary_horizon_years=40). No numbers changed (values were always 40-yr).
2. Morphology density: v1 hull-area density included degenerate hulls -> inflated/unstable
   values; v2 restricts density-hull to 152 non-degenerate clusters and adds stable
   100-m-buffer density. Density findings changed materially:
   - hull density rho -0.25 (non-degenerate only, n=152)
   - buffer density rho 0.03 p=0.49 -> prior "lower density -> higher VoF" claim DEMOTED.
3. road_density buffer rho 0.26 (new stable descriptor, all zones same sign).
4. New spatial diagnostics: Moran's I of vof_pct ~ 0 (perm p 0.23-0.77) -> negligible
   within-city spatial clustering of VoF.
5. Zero-mass split by city added (8/385, 18/96, 9/108 positive) -> pooled 94.1% zero
   driven mostly by Sano; disclosed explicitly.
All electrical/manuscript_values_v3 numbers UNCHANGED (no re-optimization).
