"""CEUS Gate 3 analysis (prespecified in
ceus_reassessment/CEUS_ADDITIONAL_ANALYSIS_PROTOCOL.md):
cluster-level urban morphology descriptors vs VoF%, cost decomposition
figure, boundary-sensitivity table. Descriptive only — no inferential
claims. All inputs are already-processed frozen files."""
import os, csv
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from scipy.stats import spearmanr

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CITIES = ["sano", "kudamatsu", "yasu"]

def hull_area(pts):
    if len(pts) < 3:
        return 0.0
    try:
        return ConvexHull(pts).volume  # 2-D: volume == area
    except Exception:
        return 0.0

rows = []
for c in CITIES:
    d = f"{ROOT}/data/processed/{c}"
    nodes = pd.read_csv(f"{d}/nodes.csv")
    edges = pd.read_csv(f"{d}/edges.csv")
    dem = pd.read_csv(f"{d}/demand_nodes.csv")
    cl = pd.read_csv(f"{d}/clusters_v2.csv")
    res = pd.read_csv(f"{d}/cluster_results_v2.csv")
    res = res[res["city"] == c]
    nmap = nodes.set_index("node")
    clmap = dict(zip(cl["node"], cl["cluster"]))
    edges["cl_u"] = edges["u"].map(clmap)
    edges["cl_v"] = edges["v"].map(clmap)
    edges = edges[edges["cl_u"] == edges["cl_v"]]
    deg = {}
    for _, r in edges.iterrows():
        deg[r["u"]] = deg.get(r["u"], 0) + 1
        deg[r["v"]] = deg.get(r["v"], 0) + 1
    dem_nodes_by_cl = dem.copy()
    dem_nodes_by_cl["cluster"] = dem_nodes_by_cl["node"].map(clmap)
    for _, r in res.iterrows():
        k = int(r["cluster"])
        dn = dem_nodes_by_cl[dem_nodes_by_cl["cluster"] == k]["node"].tolist()
        pts = nmap.loc[nmap.index.intersection(dn), ["x_m", "y_m"]].dropna().values
        sub_e = edges[edges["cl_u"] == k]
        mean_elen = sub_e["length"].mean() if len(sub_e) else np.nan
        member_nodes = set(sub_e["u"]).union(sub_e["v"]) if len(sub_e) else set()
        mdeg = np.mean([deg.get(n, 0) for n in member_nodes]) if member_nodes else np.nan
        area = hull_area(pts) / 1e6  # km^2
        centroid = pts.mean(axis=0) if len(pts) else np.array([np.nan, np.nan])
        span = float(np.mean(np.hypot(*(pts - centroid).T))) if len(pts) else np.nan
        s1npc = r.get("s1_npc_mean", np.nan)
        vof = r.get("vof_mean", np.nan)
        vof_pct = vof / s1npc * 100 if s1npc and not np.isnan(s1npc) and s1npc != 0 else np.nan
        rows.append({
            "city": c, "cluster": k, "terminals": r["terminals"],
            "coinc_kw": r["coinc_kw"], "hull_area_km2": area,
            "demand_density_kw_km2": (r["coinc_kw"] / area if area else np.nan),
            "mean_edge_len_m": mean_elen, "mean_degree": mdeg,
            "s1_length_m": r["s1_length_mean"],
            "route_len_per_terminal_m": (r["s1_length_mean"] / r["terminals"]
                                        if r["terminals"] else np.nan),
            "span_m": span,
            "s1_npc": s1npc, "vof": vof, "vof_pct": vof_pct,
            "tld": r.get("tld", np.nan),
            "s2_feasible": r.get("s2_feasible", ""),
        })
m = pd.DataFrame(rows)
m.to_csv(f"{ROOT}/analysis/CEUS_MORPHOLOGY_CLUSTER.csv", index=False)

mf = m.dropna(subset=["vof_pct"])
preds = ["terminals", "coinc_kw", "hull_area_km2", "demand_density_kw_km2",
         "mean_edge_len_m", "mean_degree", "route_len_per_terminal_m",
         "span_m", "tld"]
cors = []
for p in preds:
    rho, pv = spearmanr(mf[p], mf["vof_pct"], nan_policy="omit")
    signs = {c: np.sign(spearmanr(
        mf[mf.city == c][p], mf[mf.city == c]["vof_pct"],
        nan_policy="omit")[0]) for c in CITIES
        if len(mf[mf.city == c].dropna(subset=[p, "vof_pct"])) > 4}
    cors.append({"predictor": p, "spearman_rho_pooled": rho,
                 "spearman_p_pooled": pv, "n": len(mf),
                 "sign_by_zone": ";".join(f"{k}:{int(v)}" for k, v in signs.items())})
cor = pd.DataFrame(cors)
cor.to_csv(f"{ROOT}/analysis/CEUS_MORPHOLOGY_CORRELATIONS.csv", index=False)
print(cor.to_string(index=False))

# scatter figure: top predictors vs VoF%
sel = cor.reindex(cor["spearman_rho_pooled"].abs().sort_values(ascending=False).index).head(4)["predictor"].tolist()
labels = {"terminals": "terminals (n)", "coinc_kw": "coincident demand (kW)",
          "hull_area_km2": "cluster area (km$^2$)", "demand_density_kw_km2": "demand density (kW/km$^2$)",
          "mean_edge_len_m": "mean road-edge length (m)", "mean_degree": "mean node degree",
          "route_len_per_terminal_m": "incumbent route length per terminal (m)",
          "span_m": "mean distance to centroid (m)", "tld": "topology divergence distance"}
fig, axes = plt.subplots(1, 4, figsize=(13, 3.2))
for ax, p in zip(axes, sel):
    for c, mk in zip(CITIES, ["o", "s", "^"]):
        sub = mf[mf.city == c]
        ax.scatter(sub[p], sub["vof_pct"], marker=mk, s=22, alpha=0.75, label=c)
    ax.set_xlabel(labels.get(p, p), fontsize=9)
    ax.set_ylabel("cluster VoF (% of NPC)", fontsize=9)
    ax.tick_params(labelsize=8)
axes[0].legend(fontsize=8, frameon=False)
fig.tight_layout()
for ext in ["png", "tiff"]:
    fig.savefig(f"{ROOT}/figures/ceus_fig_morphology.{ext}", dpi=300)
plt.close(fig)

# Priority F: decomposition figure (capex vs loss component vs VoF)
bd = pd.read_csv(f"{ROOT}/analysis/BENEFIT_DECOMPOSITION.csv")
fig, ax = plt.subplots(figsize=(6.4, 3.6))
x = np.arange(len(bd))
w = 0.28
capex_d = (bd["s1_capex"] - bd["s2_capex"]) / 1e9
loss_d = ((bd["s1_plkw"] - bd["s2_plkw"]) / bd["s1_plkw"]) * 100
ax.bar(x - w, capex_d, w, label="capex diff (bn JPY)")
ax.bar(x, (bd["s1_npc"] - bd["s2_npc"]) / 1e9, w, label="NPC diff (bn JPY)")
ax.bar(x + w, loss_d, w, label="loss power diff (%)")
ax.set_xticks(x); ax.set_xticklabels(bd["city"], fontsize=9)
ax.axhline(0, color="k", lw=0.5)
ax.legend(fontsize=8, frameon=False)
ax.set_title("S1−S2 decomposition (per zone totals)", fontsize=10)
fig.tight_layout()
for ext in ["png", "tiff"]:
    fig.savefig(f"{ROOT}/figures/ceus_fig_decomposition.{ext}", dpi=300)
plt.close(fig)

# Priority C: boundary/assumption sensitivity reuse table
sens_rows = []
variants = {"v2": "scenario_results_v2.csv", "mv120": "scenario_results_mv120.csv",
            "mv200": "scenario_results_mv200.csv", "t80": "scenario_results_t80.csv",
            "t130": "scenario_results_t130.csv", "rep24": "scenario_results_rep24.csv"}
for tag, fn in variants.items():
    p = f"{ROOT}/analysis/{fn}"
    if not os.path.exists(p):
        continue
    df = pd.read_csv(p)
    for _, r in df.iterrows():
        sens_rows.append({"variant": tag, "city": r.get("city", r.get("zone")),
                          "vof_pct": r.get("vof_pct"), "ltp_pct": r.get("ltp_pct"),
                          "npc_s1_bn": r.get("s1_npc_bn")})
pd.DataFrame(sens_rows).to_csv(f"{ROOT}/analysis/CEUS_BOUNDARY_SENSITIVITY.csv", index=False)
print("done", len(mf), "clusters,", len(sens_rows), "sensitivity rows")
