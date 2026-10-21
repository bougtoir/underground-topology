# Size confounding audit (Gate 4)
Method: rank-residual partial Spearman — rank(descriptor) and rank(VoF%) each
regressed (OLS) on rank(terminals); Spearman rho of residuals.
Result: every extent/sparsity descriptor collapses to ~0 after adjustment
(span -0.011, hull_area 0.006, route/terminal -0.027, road_density -0.192,
mean_degree -0.289, mean_edge_len 0.081, buffer_density -0.063, hull_density -0.039,
coinc_kw -0.033). Terminals itself cannot be adjusted against itself (NA);
tld is mechanically coupled to size and is not an independent effect.
CONCLUSION: no independent morphology correlate survives; apparent association
was cluster-size confounding. Morphology demoted to exploratory.
