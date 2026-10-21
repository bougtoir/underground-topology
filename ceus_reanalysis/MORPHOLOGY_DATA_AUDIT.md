# Morphology data audit (Phase 1)
n = 589 clusters (sano 385, kudamatsu 96, yasu 108). Sources: demand terminal nodes
(x_m/y_m metres), road-graph edges with length_m, cluster_results_v2.

## Degenerate hulls
437/589 clusters have terminals<3 or hull area <1e-4 km2 -> hull-area density undefined.
v1 assigned density on these anyway (e.g. 1-2 terminal -> area 0 -> near-infinite or NaN
densities such as ~6.25e9 kW/km2), corrupting the pooled density correlation.
v2: demand_density_hull_kw_km2 = NaN for degenerate rows; density-hull correlation uses
only the 152 non-degenerate clusters; flagged via degenerate_hull/few_terminals.

## Stable spatial support (v2)
Union of 100-m buffers around each cluster's demand terminals (buffer_area_km2) is
degeneracy-free for n>=1. New: demand_density_buffer_kw_km2 and
road_density_km_per_km2 (road length inside buffer union / buffer area).

## Denominator consistency / missingness
- mean_edge_len_m, mean_degree: computed on road-network edges within cluster (edges
  with both endpoints in cluster), NaN when cluster has no internal road edge
  (no_road_edges flag; 262/589 -> density correlation n=327). These are ROAD-graph
  descriptors, not feeder-graph: provenance now stated in manuscript.
- route_len_per_terminal_m = s1_length_mean / terminals (both from results file).
- span_m: mean centroid distance of demand terminals, NaN if <1 terminal.
- No infinities retained in v2 outputs; zero_vof flag kept for two-part reporting.

## Feasible vs infeasible VoF=0
VoF=0 arises when (a) S2 infeasible (hard-constraint binding) or (b) S2 feasible but not
cheaper. cluster_results_v2 carries s2_feasible; reported in zero-mass audit.
