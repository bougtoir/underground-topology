"""JIS figure finishing: Figs. 3-5 regenerated from analysis outputs at 7-in width,
>=8-pt text, grayscale-safe fills (hatching), journal-neutral terminology.
Writes figures/jis_fig3_vof_zone, jis_fig4_vof_distribution, jis_fig5_decomposition (.png/.tiff, 300 dpi)."""
import os
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = f"{ROOT}/figures"; A = f"{ROOT}/analysis"
Z = ["sano", "kudamatsu", "yasu"]; ZN = {"sano": "Sano", "kudamatsu": "Kudamatsu", "yasu": "Yasu"}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.titlesize": 9, "axes.labelsize": 9,
                     "xtick.labelsize": 8.5, "ytick.labelsize": 8.5, "legend.fontsize": 8})
def save(fig, name):
    for e in ("png", "tiff"):
        kw = {"pil_kwargs": {"compression": "tiff_lzw"}} if e == "tiff" else {}
        fig.savefig(f"{FIG}/{name}.{e}", dpi=300, bbox_inches="tight", **kw)
    plt.close(fig)
sr = pd.read_csv(f"{A}/scenario_results_v2.csv").set_index("city")
mc = pd.read_csv(f"{A}/sensitivity_mc_v2.csv").set_index("city")
fe = {}
for z in Z:
    r = pd.read_csv(f"{ROOT}/data/processed/{z}/cluster_results_v2.csv")
    fe[z] = r[r.s2_feasible & (r.n_s1_feas > 0)].copy()
    fe[z]["vp"] = 100 * fe[z].vof_mean / fe[z].s1_npc_feas_mean

# Fig. 3: zone VoF vs naive contrast, equivalence band
fig, ax = plt.subplots(figsize=(7.0, 3.2))
x = np.arange(3); w = 0.36
ax.axhspan(-1, 1, color="0.88", zorder=0, label="±1% equivalence margin")
b1 = ax.bar(x - w/2, [sr.loc[z, "vof_pct"] for z in Z], w, color="0.15", label="VoF (primary, incumbent admissible)")
b2 = ax.bar(x + w/2, [mc.loc[z, "ltp_pct_mean"] for z in Z], w, color="white", ec="0.2", hatch="///",
            label="Naive contrast, Monte Carlo mean (incumbent excluded)")
for xi, z in zip(x, Z):
    ax.annotate(f"{sr.loc[z,'vof_pct']:.2f}%", (xi - w/2, sr.loc[z, "vof_pct"]), xytext=(0, 3),
                textcoords="offset points", ha="center", fontsize=8)
    v = mc.loc[z, "ltp_pct_mean"]
    ax.annotate(f"{v:.2f}%".replace("-", "−"), (xi + w/2, v), xytext=(0, 3 if v >= 0 else -11),
                textcoords="offset points", ha="center", fontsize=8)
ax.axhline(0, color="0.3", lw=0.8)
ax.set_xticks(x); ax.set_xticklabels([ZN[z] for z in Z])
ax.set_ylabel("% of like-for-like NPC"); ax.set_ylim(-11.5, 2.5)
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, frameon=False)
for s in ("top", "right"): ax.spines[s].set_visible(False)
save(fig, "jis_fig3_vof_zone")

# Fig. 4: incidence and conditional magnitude
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 3.0), gridspec_kw={"width_ratios": [1, 1.25]})
mk = {"sano": ("o", "0.1"), "kudamatsu": ("s", "0.45"), "yasu": ("^", "0.75")}
inc = [(fe[z].vp > 1e-6).mean() * 100 for z in Z]
a1.bar(range(3), inc, color=[mk[z][1] for z in Z], ec="0.1")
for i, z in enumerate(Z):
    a1.text(i, inc[i] + 0.4, f"{int((fe[z].vp > 1e-6).sum())}/{len(fe[z])}", ha="center", fontsize=8)
a1.set_xticks(range(3)); a1.set_xticklabels([ZN[z] for z in Z])
a1.set_ylabel("Feasible clusters with VoF > 0 (%)"); a1.set_title("(a) Incidence", loc="left")
npos = 0
for z in Z:
    p = fe[z][fe[z].vp > 1e-6]; npos += len(p)
    a2.scatter(p.terminals, p.vp, marker=mk[z][0], facecolor=mk[z][1], edgecolor="0.0", s=28, label=f"{ZN[z]} (n = {len(p)})")
a2.set_yscale("log"); a2.set_xlabel("Demand terminals in cluster"); a2.set_ylabel("Cluster VoF (% of cluster NPC)")
a2.set_title(f"(b) Magnitude, positive clusters (n = {npos})", loc="left"); a2.legend(frameon=False, loc="upper left", bbox_to_anchor=(1.0, 1.0))
for ax in (a1, a2):
    for s in ("top", "right"): ax.spines[s].set_visible(False)
fig.tight_layout(); save(fig, "jis_fig4_vof_distribution")

# Fig. 5: decomposition of incumbent-minus-redesign difference
H = 40; ann = (1 - 1.03 ** -H) / 0.03; EK = 25; LF = 0.35
fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.8))
for i, (ax, z) in enumerate(zip(axes, Z)):
    f = fe[z]
    dc = (f.s1_capex_mean - f.s2_capex).sum() / 1e9
    dl = (f.s1_plkw_mean - f.s2_plkw).sum() * 8760 * LF * EK * ann / 1e9
    dt = (f.s1_npc_feas_mean - f.s2_npc).sum() / 1e9
    v = [dc, dl, dt - dc - dl]; vof = f.vof_mean.sum() / 1e9
    ax.bar(range(3), v, color=["0.25", "0.55", "0.8"], ec="0.1", width=0.6)
    ax.bar(3.3, vof, color="white", ec="0.0", hatch="///", width=0.7)
    ax.axhline(0, color="0.3", lw=0.8)
    ax.set_xticks([0, 1, 2, 3.3]); ax.set_xticklabels(["Capital", "Loss", "Other", "VoF"], fontsize=8, rotation=35, ha="right")
    ax.set_title(f"({'abc'[i]}) {ZN[z]}: total {dt:.3f}".replace("-", "−"), loc="left", fontsize=8.5)
    mx = max(max(abs(np.array(v))), abs(vof), 0.004) * 1.25; ax.set_ylim(-mx, mx)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
axes[0].set_ylabel("Incumbent − redesign\n(billion JPY, 40-year NPC)")
fig.tight_layout(); save(fig, "jis_fig5_decomposition")
print("figures written")
