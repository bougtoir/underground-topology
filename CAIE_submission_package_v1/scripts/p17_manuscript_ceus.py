"""CEUS (Computers, Environment and Urban Systems, Elsevier) manuscript
DOCX. Frozen values from analysis/manuscript_values_v3.csv; new Gate-3
morphology results from analysis/CEUS_MORPHOLOGY_*.csv. Author-date
citations. No internal versions, no journal names in text."""
import csv, os
import pandas as pd
from docx import Document
from docx.shared import Pt
from docx.oxml import parse_xml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
mv = {r["key"]: r["value"] for r in
      csv.DictReader(open(f"{ROOT}/analysis/manuscript_values_v3.csv"))}
cor = pd.read_csv(f"{ROOT}/analysis/CEUS_MORPHOLOGY_CORRELATIONS.csv")
mcl = pd.read_csv(f"{ROOT}/analysis/CEUS_MORPHOLOGY_CLUSTER.csv")
bs = pd.read_csv(f"{ROOT}/analysis/CEUS_BOUNDARY_SENSITIVITY.csv")

def fmt(v, nd=2):
    try:
        return f"{float(v):.{nd}f}"
    except Exception:
        return str(v)

def rho_of(p):
    return float(cor.loc[cor.predictor == p, "spearman_rho_pooled"].iloc[0])

doc = Document()
st = doc.styles["Normal"]; st.font.name = "Times New Roman"; st.font.size = Pt(12)

def omml(latexlike):
    return parse_xml(
        '<m:oMathPara xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">'
        f'<m:oMath><m:r><m:t>{latexlike}</m:t></m:r></m:oMath></m:oMathPara>')

def eq(text):
    p = doc.add_paragraph()
    p._p.append(omml(text))

def cite(par, text):
    par.add_run(f"({text})")

NCL = int(float(mv["sano_clusters"])+float(mv["kudamatsu_clusters"])+float(mv["yasu_clusters"]))
NFEAS = int(float(mv["sano_clusters_feasible"])+float(mv["kudamatsu_clusters_feasible"])+float(mv["yasu_clusters_feasible"]))
DEM = float(mv["sano_lv_demand_mw"])+float(mv["kudamatsu_lv_demand_mw"])+float(mv["yasu_lv_demand_mw"])
NMORPH = int(mcl.dropna(subset=["vof_pct"]).shape[0])
ZEROVOF = float((mcl["vof_pct"] <= 0).mean()) * 100

doc.add_heading("The Value of Topology Flexibility at Infrastructure "
                "Renewal: A Feasibility-Gated Geospatial Assessment of "
                "Low-Voltage Re-Layout During Undergrounding", 0)
doc.add_paragraph("[Author and affiliation to be completed at submission]")
doc.add_paragraph("Corresponding author: [to be completed at submission]")

doc.add_heading("Abstract", 1)
doc.add_paragraph(
    "Urban renewal programs that replace aging overhead distribution "
    "lines with underground cables face a rarely asked spatial question: "
    "when the corridor is already committed, is re-drawing the local "
    "network worth anything? This study quantifies the value of topology "
    "flexibility (VoF) at renewal as a geospatial decision problem. "
    "Legacy low-voltage networks are reconstructed from open municipal "
    "and OpenStreetMap data in three Japanese study zones spanning three "
    "observability tiers; candidate re-layouts are synthesized as "
    "weighted Steiner trees on the road graph under explicit engineering "
    "feasibility gates (coincident-load sizing, ampacity, ~150 kVA "
    "transformer zones, 6% voltage-drop limit) with AC power-flow "
    "validation on every feasible synthesized feeder. Across "
    f"{NFEAS} feasible feeder clusters serving {fmt(DEM,1)} MW of modeled "
    "demand, VoF is "
    f"{fmt(mv['sano_vof_pct'],2)}%, {fmt(mv['kudamatsu_vof_pct'],2)}%, and "
    f"{fmt(mv['yasu_vof_pct'],2)}% of like-for-like life-cycle cost — "
    "inside a prespecified 1% practical-equivalence margin. At "
    f"{NMORPH} feeder-cluster scale, residual flexibility value "
    "concentrates in larger, spatially sparser, lower-demand-density "
    "clusters (descriptive, "
    f"{fmt(ZEROVOF,0)}% of clusters show zero value). Like-for-like "
    "renewal is a defensible default at this scale; the transferable "
    "contribution is the screening method, not the magnitudes.")
doc.add_paragraph("Keywords: urban infrastructure; undergrounding; "
                  "geospatial decision support; network reconstruction; "
                  "urban morphology; life-cycle cost; Steiner tree")

doc.add_heading("1. Introduction", 1)
p = doc.add_paragraph(
    "A large share of urban infrastructure is invisible: electricity, "
    "water and communications networks buried beneath or strung above "
    "streets are only partially recorded, and their spatial form is "
    "known approximately at best. As cities worldwide renew aging "
    "overhead distribution by undergrounding, each renewal project opens "
    "a bounded but real design choice: keep the inherited low-voltage "
    "layout, or use the committed civil works to re-route it. Whether "
    "that option is worth exercising is a question of urban spatial "
    "structure, network physics and life-cycle economics at once — yet "
    "the literatures that own each of those pieces have barely met. "
    "Urban morphology research has built a mature quantitative "
    "vocabulary for street and settlement form ")
cite(p, "Barthélemy, 2011")
p.add_run("; ")
cite(p, "Cardillo et al., 2006")
p.add_run("; ")
cite(p, "Louf and Barthélemy, 2014")
p.add_run("; ")
cite(p, "Boeing, 2018")
p.add_run("; ")
cite(p, "Levinson, 2012")
p.add_run(", and geospatial work has shown that infrastructure networks "
    "co-located with urban form carry morphology-dependent structure ")
cite(p, "Abdel-Mottaleb and Zhang, 2020")
p.add_run(". Parallel work on hidden utility networks reconstructs "
    "their geospatial topology from proxies — street-view imagery, "
    "design rules, open GIS data ")
cite(p, "Zhang et al., 2025")
p.add_run("; ")
cite(p, "Abhilash Bandam et al., 2021")
p.add_run("; "); cite(p, "Liu et al., 2025"); p.add_run("; ")
cite(p, "Babli et al., 2025")
p.add_run(" — and spatial-network models explain how such systems grow ")
cite(p, "Fu et al., 2016")
p.add_run(". What neither stream does is treat the reconstructed "
    "network as an object of decision: how much is the option to "
    "re-layout worth, conditional on the spatial structure actually "
    "inherited?")
p = doc.add_paragraph(
    "This paper poses that question for undergrounding renewal. "
    "Economics work already shows undergrounding fails cost-benefit "
    "tests as a blanket policy ")
cite(p, "Fenrick and Getachew, 2012")
p.add_run("; ")
cite(p, "Larsen, 2016")
p.add_run(", while resilience-oriented studies find targeted "
    "undergrounding can pay ")
cite(p, "Taheri et al., 2023")
p.add_run(". But inside a committed undergrounding program a different "
    "marginal question remains: does re-drawing the network at renewal "
    "beat like-for-like replacement? Distribution-planning methods "
    "optimize feeder routing against a fixed or greenfield demand "
    "surface ")
cite(p, "Samui et al., 2012")
p.add_run("; ")
cite(p, "Kumar et al., 2014")
p.add_run("; ")
cite(p, "Camargo et al., 2013")
p.add_run("; ")
cite(p, "Tram and Wall, 1988")
p.add_run("; ")
cite(p, "Baran and Wu, 1989a, 1989b")
p.add_run("; none frames the renewal window as a choice set in which "
    "the incumbent remains admissible.")
p = doc.add_paragraph(
    "We formulate renewal as exactly that choice set. The estimand is "
    "the value of topology flexibility (VoF): the mean over legacy "
    "reconstruction replicates of max(0, NPC(replicate) − NPC(best "
    "feasible redesign)), a nonnegative measure in which retaining the "
    "incumbent is an admissible decision rather than a forced redesign. "
    "This estimand design separates an honest option value from the "
    "inflated savings that appear when incumbent layouts are excluded "
    "from the comparison. We then ask a specifically urban question "
    "that turns the estimand into a geospatial hypothesis: is residual "
    "flexibility value uniform, or does it concentrate where urban "
    "morphology leaves routing slack? Using the street-network and "
    "settlement descriptors standard in quantitative urban morphology, "
    "we show that value — where it exists at all — concentrates "
    "systematically in larger, sparser, lower-density feeder clusters. "
    "The contribution is threefold: (i) a feasibility-gated, "
    "incumbent-admissible estimand for renewal-time network decisions; "
    "(ii) an open-data reconstruction pipeline spanning three "
    "observability tiers with AC-validated electrical constraints; and "
    "(iii) evidence that the option value of re-layout is both bounded "
    "(<0.5% of life-cycle cost) and spatially structured — a screening "
    "rule for where re-layout assessment is worth its engineering cost. "
    "Figure 1 summarizes the data-to-decision pipeline.")

doc.add_heading("2. Data and methods", 1)
doc.add_heading("2.1 Study zones and data tiers", 2)
doc.add_paragraph(
    "Three Japanese municipalities were selected for complementary data "
    "tiers rather than representativeness of Japan as a whole (Table 1). "
    "Sano (Tier 1) provides security-light inventories carrying pole "
    "identifiers and coordinates; Kudamatsu (Tier 2) provides geolocated "
    "security-light anchors without pole linkage; Yasu (Tier 3) provides "
    "road and building geometry only. Within each municipality a compact "
    "study zone was extracted as the largest connected component of the "
    "OpenStreetMap road graph ")
p = doc.paragraphs[-1]
cite(p, "Haklay and Weber, 2008")
p.add_run(" (Figure 2), and building footprints were "
    "assigned estimated peak demand (30–60 W/m², two floors assumed) and "
    "snapped to the nearest road node. Buildings whose estimated raw "
    "peak exceeds 150 kW are marked medium-voltage-served and excluded "
    "from LV synthesis; this removes "
    f'{fmt(mv["sano_mv_demand_mw"],1)}, {fmt(mv["kudamatsu_mv_demand_mw"],1)}, and '
    f'{fmt(mv["yasu_mv_demand_mw"],1)} MW respectively. All distances use '
    "projected metric coordinates; mean building-to-road snap distances "
    "are 37–49 m and are disclosed as modeled-demand-surface error.")
doc.add_heading("2.2 Legacy network reconstruction", 2)
p = doc.add_paragraph(
    "Because actual LV cable routing is unobserved, legacy topologies "
    "are reconstructed as an ensemble under each tier's evidence: "
    "geo-referenced LV synthesis from open data follows the precedent "
    "of ")
cite(p, "Abhilash Bandam et al., 2021")
p.add_run("; ")
cite(p, "Zhang et al., 2025")
p.add_run("; "); cite(p, "Liu et al., 2025"); p.add_run("; ")
cite(p, "Babli et al., 2025")
p.add_run(", using security-light anchors as demand-side routing "
    "priors (never equated with pole or cable locations) and the road "
    "graph as the admissible conduit space. Feeder clusters are formed "
    "under a ~150 kVA transformer-zone constraint; 24-replicate and "
    "leave-one-family-out ensembles carry reconstruction uncertainty "
    "forward rather than collapsing it.")
doc.add_heading("2.3 Engineering feasibility and electrical model", 2)
p = doc.add_paragraph(
    "All synthesized topologies are gated by engineering feasibility "
    "before any cost comparison: 415 V radial feeders, coincident peak "
    "load, ampacity, transformer loading, and a 6% voltage-drop limit. "
    "The linearized branch-flow model ")
cite(p, "Gan and Low, 2014")
p.add_run(" was validated against pandapower AC power flow ")
cite(p, "Thurner et al., 2018")
p.add_run(" on all feasible synthesized feeders; the agreement bounds "
    "the surrogate's error on the modeled objects (it does not validate "
    "them as the real municipal networks).")
doc.add_heading("2.4 Re-layout optimization and the VoF estimand", 2)
doc.add_paragraph(
    "Re-layout is formulated as weighted Steiner-tree synthesis on the "
    "road graph with per-edge conductor sizing, approximated by a fast "
    "Steiner heuristic")
p = doc.paragraphs[-1]
cite(p, "Kou et al., 1981")
p.add_run("; ")
cite(p, "Hwang and Richards, 1992")
p.add_run(". Candidate sets are enumerated per feeder cluster; the "
    "incumbent-like replicate remains in the admissible set. Life-cycle "
    "cost NPC combines trenching/cable capex and 40-year discounted "
    "losses at frozen engineering prices. The primary estimand is")
eq("VoF = mean_r max(0, NPC(S1_r) - min_c∈feasible NPC(c))")
doc.add_paragraph(
    "a nonnegative quantity: zero whenever no feasible redesign beats "
    "the incumbent. For transparency we also report the conventional "
    "naive ΔNPC contrast (S1 mean vs S2 best, incumbent excluded) as a "
    "secondary statistic whose artifact-proneness is part of the "
    "findings.")
doc.add_heading("2.5 Urban morphology descriptors", 2)
doc.add_paragraph(
    "At feeder-cluster scale we compute a prespecified, interpretable "
    "descriptor set from the processed road graph and demand surface: "
    "number of demand terminals, coincident demand (kW), convex-hull "
    "area (km²), demand density (kW/km²), mean road-edge length (m), "
    "mean node degree, incumbent route length per terminal (m), and "
    "mean distance to the demand centroid (m) — metrics in the tradition "
    "of planar-graph street-network analysis ")
p = doc.paragraphs[-1]
cite(p, "Cardillo et al., 2006")
p.add_run("; ")
cite(p, "Barthélemy, 2011")
p.add_run("; ")
cite(p, "Boeing, 2018")
p.add_run(". Their association with cluster VoF is assessed "
    "descriptively (Spearman rank summaries plus within-zone sign "
    "consistency); clusters nested in three purposive zones are not "
    "treated as independent city samples.")

doc.add_heading("3. Results", 1)
doc.add_paragraph(
    f'Table 2 summarizes {NCL} clusters ({NFEAS} feasible) serving '
    f'{fmt(DEM,1)} MW of modeled LV peak demand — '
    f'{fmt(mv["sano_lv_share_total_pct"],0)}%, {fmt(mv["kudamatsu_lv_share_total_pct"],0)}%, '
    f'and {fmt(mv["yasu_lv_share_total_pct"],0)}% of total zone demand in '
    "Sano/Kudamatsu/Yasu (the remainder is MV-served by design and cancels "
    "in contrasts). Figure 3 shows a representative feeder cluster under "
    "the like-for-like replicate and the optimized layout. The primary "
    "VoF estimand gives "
    f'{fmt(mv["sano_vof_pct"],2)}%, {fmt(mv["kudamatsu_vof_pct"],2)}%, and '
    f'{fmt(mv["yasu_vof_pct"],2)}% of like-for-like NPC — all inside the '
    "prespecified 1% practical-equivalence margin (Figure 4). The "
    "secondary naive contrast gives "
    f'{fmt(mv["sano_ltp_pct"],2)}%, {fmt(mv["kudamatsu_ltp_pct"],1)}%, and '
    f'{fmt(mv["yasu_ltp_pct"],2)}%; the negative Kudamatsu value is an '
    "estimand artifact (incumbent excluded from the candidate set) and is "
    "not robust to the LV/MV boundary assumption (Table 4). AC validation "
    "on all feasible synthesized feeders gives max voltage-magnitude "
    f'deviation {fmt(mv["ac_vm_abs_max"],3)} pu against a 0.02 tolerance '
    f'and feasibility agreement {fmt(mv["ac_feas_agreement"],2)} over '
    f'{fmt(mv["ac_n_feeders"],0)} feeders.')
doc.add_paragraph(
    f"At feeder-cluster scale ({NMORPH} feasible clusters), VoF is "
    f"zero for {fmt(ZEROVOF,0)}% of clusters — the option value is "
    "concentrated, not diffuse. Where nonzero, it associates "
    "descriptively with urban spatial structure (Figure 5, Table 3): "
    f"pooled Spearman ρ = {rho_of('hull_area_km2'):.2f} for cluster "
    f"area, {rho_of('span_m'):.2f} for spatial span, "
    f"{rho_of('route_len_per_terminal_m'):.2f} for incumbent route "
    f"length per terminal, {rho_of('terminals'):.2f} for terminal "
    f"count, and {rho_of('demand_density_kw_km2'):.2f} for demand "
    "density, with the same sign in all three zones. Larger, "
    "spatially more dispersed, lower-density clusters retain more "
    "re-layout slack; compact high-density clusters are already "
    "near-optimal. Cost decomposition (Figure 6) shows the small net "
    "VoF arises from offsetting excavation-length savings and "
    "loss-related changes rather than any single dominant channel, "
    "consistent with the bounded estimand interpretation.")

doc.add_heading("4. Discussion", 1)
p = doc.add_paragraph(
    "The finding is bounded and geographically interpretable. Relative "
    "to reconstruction work that maps hidden utility networks ")
cite(p, "Zhang et al., 2025")
p.add_run("; ")
cite(p, "Abhilash Bandam et al., 2021")
p.add_run("; "); cite(p, "Liu et al., 2025"); p.add_run("; ")
cite(p, "Babli et al., 2025")
p.add_run(" this study adds the decision layer those maps feed into: "
    "the reconstruction is not the answer, it is the choice set over "
    "which a renewal option is priced, and feasibility gating decides "
    "which reconstructed alternatives are physically realizable. "
    "Relative to system-level undergrounding economics ")
cite(p, "Larsen, 2016")
p.add_run("; ")
cite(p, "Fenrick and Getachew, 2012")
p.add_run(" the result sharpens the 'undergrounding is rarely "
    "cost-effective' conclusion: even once the corridor is paid for, "
    "the incumbent layout is already near the life-cycle optimum, so "
    "the residual value of re-design is small — and it is spatially "
    "concentrated in the same morphology-dependent way that "
    "co-located infrastructure connectivity is ")
cite(p, "Abdel-Mottaleb and Zhang, 2020")
p.add_run(". The morphology association is descriptive and "
    "zero-inflation-driven "
    f"({fmt(ZEROVOF,0)}% of clusters have no flexibility value); we "
    "present it as a screening heuristic for where detailed re-layout "
    "engineering is worth commissioning, not as a predictive model.")
doc.add_paragraph(
    "Two methodological controls produce the bounded result. First, "
    "feasibility gating: treating ~350 kW of raw building peaks as one "
    "undiversified LV load produces physically impossible feeders "
    "(double-digit voltage drops) and manufactures fictitious headroom. "
    "Second, estimand design: the negative Kudamatsu ΔNPC is an "
    "incumbent-exclusion artifact and is sensitive to the LV/MV "
    "boundary assumption (Table 4); under the optional estimand all "
    "zones stay inside the practical-equivalence margin. Mechanistically "
    "the negative contrast traces to a few small wide-area clusters "
    "where any rewiring costs 2–10× the incumbent corridor with no "
    "compensating loss reduction.")
doc.add_paragraph(
    "Limitations. Reconstructed topologies are modeled objects: anchor "
    "data do not observe actual pole-to-pole routing, and results are "
    "conditional on the reconstruction ensemble (stability checked by "
    "24-replicate and leave-one-family-out). Study zones are compact "
    "extractions chosen for data-tier contrast, not city samples; OSM "
    "completeness is unverified; demand, coincidence, the 6% drop limit "
    "and the 150 kW LV/MV boundary are assumptions, several of which "
    "materially move the secondary contrast though not the VoF "
    "ordering. Morphology associations are descriptive over 589 "
    "spatially dependent clusters in three zones — transferable as a "
    "screening pattern, not as coefficients. MV-served demand is "
    "excluded by design; municipality-facing outputs are "
    "planning-support estimates, not engineering designs.")

doc.add_heading("5. Conclusions", 1)
doc.add_paragraph(
    "Urban renewal is a spatial decision, and the option to re-draw "
    "hidden infrastructure can be priced. Under feasibility-gated "
    "reconstruction and an incumbent-admissible estimand, renewal-time "
    "topology re-optimization is economically equivalent to "
    "like-for-like renewal in all three study zones "
    f"(VoF {fmt(mv['sano_vof_pct'],2)}–{fmt(mv['kudamatsu_vof_pct'],2)}% "
    "of life-cycle cost). What little flexibility value remains is "
    "spatially structured: it concentrates in larger, sparser, "
    "lower-density feeder clusters. The transferable outputs are the "
    "screening estimand and the reconstruction-plus-gating pipeline; "
    "the magnitudes are zone-specific modeled results.")

doc.add_heading("Acknowledgements", 1)
doc.add_paragraph("[to be completed at submission]")

doc.add_heading("Declarations", 1)
doc.add_paragraph("Declaration of generative AI: during the preparation "
                  "of this work the author used an AI coding assistant "
                  "for code scaffolding and drafting. The author "
                  "reviewed and edited all content and takes full "
                  "responsibility for the publication.")
doc.add_paragraph("Data availability: all scripts, the source registry, "
                  "checksums, and machine-readable result tables are "
                  "provided in the supplementary repository snapshot "
                  "(github.com/bougtoir/underground-topology-segan). "
                  "Municipal open data were used under their stated "
                  "licenses (CC-BY for Kudamatsu); OpenStreetMap data "
                  "under ODbL.")
doc.add_paragraph("Conflict of interest: none declared. Funding: none.")

doc.add_heading("Figure captions (figures supplied as separate files)", 1)
for cap in [
    "Figure 1. Data-to-decision pipeline: open geospatial inputs, zone construction, feasibility-gated reconstruction, and the incumbent-admissible renewal decision model.",
    "Figure 2. Study zones: road graph (grey) and snapped building demand nodes (blue).",
    "Figure 3. Example feeder cluster: S1 like-for-like replicate vs S2 optimized layout.",
    "Figure 4. Primary estimand VoF by zone vs Monte-Carlo mean of the secondary naive ΔNPC; band = prespecified 1% practical-equivalence margin.",
    "Figure 5. Cluster-level VoF vs prespecified urban morphology descriptors (589 clusters, three zones; descriptive Spearman summaries, spatially dependent units; 94% of clusters have zero VoF).",
    "Figure 6. S1−S2 cost decomposition per zone: capex difference, NPC difference, and loss-power difference (accounting decomposition of modeled totals).",
]:
    doc.add_paragraph(cap)

doc.add_heading("Tables", 1)
doc.add_paragraph("Table 1. Study zones and data tiers")
t1 = doc.add_table(rows=4, cols=5); t1.style = "Table Grid"
hdr = ["Zone","Tier","LV demand (MW)","MV-excluded (MW)","Feasible clusters"]
for i, h in enumerate(hdr): t1.rows[0].cells[i].text = h
rows1 = [["Sano","1 (pole-ID linked anchors)",fmt(mv["sano_lv_demand_mw"],1),fmt(mv["sano_mv_demand_mw"],1),str(int(float(mv["sano_clusters_feasible"])))],
         ["Kudamatsu","2 (geolocated anchors)",fmt(mv["kudamatsu_lv_demand_mw"],1),fmt(mv["kudamatsu_mv_demand_mw"],1),str(int(float(mv["kudamatsu_clusters_feasible"])))],
         ["Yasu","3 (roads/buildings only)",fmt(mv["yasu_lv_demand_mw"],1),fmt(mv["yasu_mv_demand_mw"],1),str(int(float(mv["yasu_clusters_feasible"])))]]
for r,row in enumerate(rows1,1):
    for c,v in enumerate(row): t1.rows[r].cells[c].text = v

doc.add_paragraph("Table 2. Scenario results (feasibility-gated)")
t2 = doc.add_table(rows=4, cols=10); t2.style = "Table Grid"
hdr2 = ["city","clusters","feasible","demand MW","S1 NPC (bn JPY)","S2 NPC","VoF (bn JPY)","VoF % (primary)","ΔNPC bn (secondary)","ΔNPC % (secondary)"]
for i, h in enumerate(hdr2): t2.rows[0].cells[i].text = h
def ltp_bn(c):
    return float(mv[f"{c}_s1_npc_bn"]) - float(mv[f"{c}_s2_npc_bn"])
rows2 = [["sano",str(int(float(mv["sano_clusters"]))),str(int(float(mv["sano_clusters_feasible"]))),fmt(mv["sano_lv_demand_mw"],1),fmt(mv["sano_s1_npc_bn"],2),fmt(mv["sano_s2_npc_bn"],2),fmt(mv["sano_vof_bn"],4),fmt(mv["sano_vof_pct"],3),f"{ltp_bn('sano'):.3f}",fmt(mv["sano_ltp_pct"],2)],
         ["kudamatsu",str(int(float(mv["kudamatsu_clusters"]))),str(int(float(mv["kudamatsu_clusters_feasible"]))),fmt(mv["kudamatsu_lv_demand_mw"],1),fmt(mv["kudamatsu_s1_npc_bn"],2),fmt(mv["kudamatsu_s2_npc_bn"],2),fmt(mv["kudamatsu_vof_bn"],4),fmt(mv["kudamatsu_vof_pct"],3),f"{ltp_bn('kudamatsu'):.3f}",fmt(mv["kudamatsu_ltp_pct"],1)],
         ["yasu",str(int(float(mv["yasu_clusters"]))),str(int(float(mv["yasu_clusters_feasible"]))),fmt(mv["yasu_lv_demand_mw"],1),fmt(mv["yasu_s1_npc_bn"],2),fmt(mv["yasu_s2_npc_bn"],2),fmt(mv["yasu_vof_bn"],4),fmt(mv["yasu_vof_pct"],3),f"{ltp_bn('yasu'):.3f}",fmt(mv["yasu_ltp_pct"],2)]]
for r,row in enumerate(rows2,1):
    for c,v in enumerate(row): t2.rows[r].cells[c].text = v

doc.add_paragraph("Table 3. Cluster-level morphology descriptors vs VoF "
                  "(pooled Spearman ρ; sign consistent in all 3 zones "
                  "for every descriptor; n=589, spatially dependent, "
                  "descriptive only)")
t3 = doc.add_table(rows=len(cor)+1, cols=3); t3.style = "Table Grid"
for i,h in enumerate(["descriptor","Spearman ρ (pooled)","sign by zone (sano/kudamatsu/yasu)"]):
    t3.rows[0].cells[i].text = h
for r,(_,rr) in enumerate(cor.iterrows(),1):
    t3.rows[r].cells[0].text = str(rr["predictor"])
    t3.rows[r].cells[1].text = f"{rr['spearman_rho_pooled']:.3f}"
    t3.rows[r].cells[2].text = str(rr["sign_by_zone"])

doc.add_paragraph("Table 4. Boundary/parameter sensitivity (reused "
                  "frozen variants: VoF% primary | naive ΔNPC% secondary)")
vtags = {"v2":"baseline","mv120":"MV threshold 120 kW","mv200":"MV threshold 200 kW",
         "t80":"transformer 80 kVA","t130":"transformer 130 kVA","rep24":"24-replicate ensemble"}
t4 = doc.add_table(rows=len(bs)+1, cols=4); t4.style = "Table Grid"
for i,h in enumerate(["variant","city","VoF %","naive ΔNPC %"]):
    t4.rows[0].cells[i].text = h
for r,(_,rr) in enumerate(bs.iterrows(),1):
    t4.rows[r].cells[0].text = vtags.get(rr["variant"], str(rr["variant"]))
    t4.rows[r].cells[1].text = str(rr["city"])
    t4.rows[r].cells[2].text = fmt(rr["vof_pct"],3)
    t4.rows[r].cells[3].text = fmt(rr["ltp_pct"],2)

doc.add_heading("References", 1)
REFS = [
 "Abhilash Bandam, Syranidou, C., Linssen, J. and Stolten, D. (2021). "
 "Geo-referenced synthetic low-voltage distribution networks: a "
 "data-driven approach. 2021 IEEE PES Innovative Smart Grid "
 "Technologies Europe (ISGT Europe), pp. 244–249. "
 "doi:10.1109/ISGTEurope52324.2021.9639916",
 "Babli, M., Gebhard, T. and Brucherseifer, E. (2025). Open data-driven "
 "reconstruction of power distribution grid: a land use-based approach. "
 "Electronics 14(7): 1414. doi:10.3390/electronics14071414",
 "Baran, M.E. and Wu, F.F. (1989a). Network reconfiguration in "
 "distribution systems for loss reduction and load balancing. IEEE "
 "Transactions on Power Delivery 4(2): 1401–1407. doi:10.1109/61.25627",
 "Baran, M.E. and Wu, F.F. (1989b). Optimal capacitor placement on "
 "radial distribution systems. IEEE Transactions on Power Delivery "
 "4(1): 725–734. doi:10.1109/61.19265",
 "Barthélemy, M. (2011). Spatial networks. Physics Reports 499(1–3): "
 "1–101. doi:10.1016/j.physrep.2010.11.002",
 "Boeing, G. (2018). A multi-scale analysis of 27,000 urban street "
 "networks: every US city, town, urbanized area, and Zillow "
 "neighborhood. Environment and Planning B: Urban Analytics and City "
 "Science 47(4): 590–615. doi:10.1177/2399808318784595",
 "Camargo, V., Lavorato, M. and Romero, R. (2013). Specialized genetic "
 "algorithm to solve the electrical distribution system expansion "
 "planning. 2013 IEEE Power & Energy Society General Meeting, pp. 1–5. "
 "doi:10.1109/PESMG.2013.6672615",
 "Cardillo, A., Scellato, S., Latora, V. and Porta, S. (2006). "
 "Structural properties of planar graphs of urban street patterns. "
 "Physical Review E 73(6): 066107. doi:10.1103/PhysRevE.73.066107",
 "Fenrick, S.A. and Getachew, L. (2012). Cost and reliability "
 "comparisons of underground and overhead power lines. Utilities "
 "Policy 20(1): 31–37. doi:10.1016/j.jup.2011.10.002",
 "Fu, G., Wilkinson, S. and Dawson, R. (2016). A spatial network "
 "model for civil infrastructure system development. Computer-Aided "
 "Civil and Infrastructure Engineering 31(9): 661–680. "
 "doi:10.1111/mice.12204",
 "Gan, L. and Low, S.H. (2014). Convex relaxations and linear "
 "approximation for optimal power flow in multiphase radial networks. "
 "2014 Power Systems Computation Conference, pp. 1–9. "
 "doi:10.1109/PSCC.2014.7038399",
 "Haklay, M. and Weber, P. (2008). OpenStreetMap: user-generated "
 "street maps. IEEE Pervasive Computing 7(4): 12–18. "
 "doi:10.1109/MPRV.2008.80",
 "Hwang, F.K. and Richards, D.S. (1992). Steiner tree problems. "
 "Networks 22(1): 55–89. doi:10.1002/net.3230220105",
 "Kou, L., Markowsky, G. and Berman, L. (1981). A fast algorithm for "
 "Steiner trees. Acta Informatica 15(2): 141–145. "
 "doi:10.1007/BF00288961",
 "Kumar, D., Samantaray, S.R. and Joos, G. (2014). A reliability "
 "assessment based graph theoretical approach for feeder routing in "
 "power distribution networks including distributed generations. "
 "International Journal of Electrical Power & Energy Systems 57: "
 "11–30. doi:10.1016/j.ijepes.2013.11.039",
 "Larsen, P.H. (2016). A method to estimate the costs and benefits of "
 "undergrounding electricity transmission and distribution lines. "
 "Energy Economics 60: 47–61. doi:10.1016/j.eneco.2016.09.011",
 "Levinson, D. (2012). Network structure and city size. PLoS ONE "
 "7(1): e29721. doi:10.1371/journal.pone.0029721",
 "Liu, Y., et al. (2025). Topology identification and parameters "
 "estimation of LV distribution networks using open GIS data. TNO "
 "publication, full text at publications.tno.nl (record verified; "
 "journal DOI pending).",
 "Louf, R. and Barthélemy, M. (2014). A typology of street patterns. "
 "Journal of The Royal Society Interface 11(101): 20140924. "
 "doi:10.1098/rsif.2014.0924",
 "Samui, A., Singh, S., Ghose, T. and Samantaray, S.R. (2012). A "
 "direct approach to optimal feeder routing for radial distribution "
 "system. IEEE Transactions on Power Delivery 27(1): 253–260. "
 "doi:10.1109/TPWRD.2011.2167522",
 "Taheri, B., Molzahn, D.K. and Grijalva, S. (2023). Improving "
 "distribution system resilience by undergrounding lines and "
 "deploying mobile generators. Electric Power Systems Research 214: "
 "108804. doi:10.1016/j.epsr.2022.108804",
 "Thurner, L., Scheidler, A., Schafer, F., Menke, J.-H., Dollichon, "
 "J., Meier, F., Meinecke, S. and Braun, M. (2018). Pandapower — an "
 "open-source Python tool for convenient modeling, analysis, and "
 "optimization of electric power systems. IEEE Transactions on Power "
 "Systems 33(6): 6510–6521. doi:10.1109/TPWRS.2018.2829021",
 "Tram, H.N. and Wall, D.L. (1988). Optimal conductor selection in "
 "planning radial distribution systems. IEEE Transactions on Power "
 "Systems 3(1): 200–206. doi:10.1109/59.43199",
 "Zhang, F., Xu, Z., Zhu, R., Liang, C. and Gu, D. (2025). "
 "Geospatial mapping of urban utility networks integrating street "
 "view images and design rules. Computer-Aided Civil and "
 "Infrastructure Engineering 40(27): 4884–4903. "
 "doi:10.1111/mice.70085",
 "Abdel-Mottaleb, N. and Zhang, Q. (2020). Water distribution–transportation "
 "interface connectivity responding to urban geospatial morphology. "
 "Journal of Infrastructure Systems 26(3): 04020025. "
 "doi:10.1061/(ASCE)IS.1943-555X.0000563",
]
for r in REFS:
    doc.add_paragraph(r)

out = f"{ROOT}/manuscript/manuscript_ceus_v1.docx"
doc.save(out)
print("saved", out, "| refs:", len(REFS))
