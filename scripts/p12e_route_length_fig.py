"""Regenerate manuscript Figure 3 (S2 vs S1 route length, log-log).

Re-creates the canonical route-length comparison committed as
figures/ceus_fig_routelength.png. Source data: per-cluster results
data/processed/<city>/cluster_results_v2.csv (incumbent s1_length_mean vs
optimized s2_length on the both-replicate-feasible cohort filter used by
the AC validation and decomposition figures).
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = f"{ROOT}/figures"
CITIES = ["sano", "kudamatsu", "yasu"]
CNAMES = {"sano": "sano", "kudamatsu": "kudamatsu", "yasu": "yasu"}
MARK = {"sano": ("o", "tab:blue"), "kudamatsu": ("s", "tab:orange"),
        "yasu": ("^", "tab:green")}

plt.rcParams.update({"figure.dpi": 300, "savefig.dpi": 300})
fig, ax = plt.subplots(figsize=(4.6, 3.9))
n_off = 0
n_tot = 0
for c in CITIES:
    d = pd.read_csv(f"{ROOT}/data/processed/{c}/cluster_results_v2.csv")
    f = d[(d.s2_feasible == True) & (d.n_s1_feas > 0)].copy()
    f["s1_len"] = f.s1_length_mean.clip(lower=1.0)
    f["s2_len"] = f.s2_length.clip(lower=1.0)
    m, col = MARK[c]
    ax.scatter(f.s1_len, f.s2_len, s=26, marker=m, alpha=0.55, c=col,
               edgecolors="none", label=f"{CNAMES[c]} (n={len(f)})")
    n_off += int((abs(f.s2_length - f.s1_length_mean) > 1.0).sum())
    n_tot += len(f)
lims = [1, 2e3]
ax.plot(lims, lims, "k--", lw=0.8)
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(lims); ax.set_ylim(lims)
ax.set_xlabel("incumbent route length S1 (m)")
ax.set_ylabel("optimized route length S2 (m)")
ax.legend(fontsize=8, loc="upper left", framealpha=0.9)
ax.set_title("Re-layout changes are rare: S2 vs S1 route length\n"
             f"({n_off}/{n_tot} feasible clusters alter the corridor by >1 m)",
             fontsize=9.5)
fig.tight_layout()
for ext in ["png", "tiff"]:
    fig.savefig(f"{FIG}/ceus_fig_routelength.{ext}", dpi=300, bbox_inches="tight")
plt.close(fig)
print(f"wrote ceus_fig_routelength (off-corridor {n_off}/{n_tot})")
