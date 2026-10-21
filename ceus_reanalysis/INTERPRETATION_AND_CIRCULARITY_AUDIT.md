# Circularity audit (Phase 4)
Descriptors split into two classes; manuscript text keeps them distinct:
(a) Independent urban-structure inputs: demand-terminal coincidence (coinc_kw),
    demand density on fixed buffer support, road-network density within the cluster
    catchment (buffer union). These do not depend on S1/S2 outcomes.
(b) Objective-linked descriptors: route_len_per_terminal_m and tld derive from the
    S1 result or the same road graph the optimizer traverses -> they are diagnostics of
    where S1 is congested, NOT causal drivers of VoF. Manuscript states this verbatim.
Mechanical relationship note: hull_area/span correlate with route-length partly because
bigger service areas need more feeder metres — associations are descriptive.
Falsification check applied: hull-area density's negative pooled correlation (rho=-0.25
on 152 non-degenerate rows) does NOT survive moving to stable buffer support
(buffer density rho=0.03, p=0.49). Reported honestly: density-based claims demoted;
extent/sparsity descriptors (hull_area among non-degenerate, span, route/terminal,
terminals, road density) retain consistent sign across all three zones.
