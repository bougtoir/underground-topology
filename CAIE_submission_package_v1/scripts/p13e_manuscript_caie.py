"""Post-SEGAN retarget: CAIE (Computer-Aided Civil and Infrastructure
Engineering, Wiley) manuscript DOCX. Frozen values from
analysis/manuscript_values_v3.csv. Author-date citations (Wiley style).
Changes vs v4 SEGAN version: reframed intro/discussion toward
infrastructure renewal planning and decision analysis; +5 verified
references; 'pre-registered' -> 'prespecified'; no smart-grid framing."""
import csv, os
import pandas as pd
from docx import Document
from docx.shared import Pt
from docx.oxml import parse_xml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
mv = {r["key"]: r["value"] for r in
      csv.DictReader(open(f"{ROOT}/analysis/manuscript_values_v3.csv"))}

def fmt(v, nd=2):
    try:
        return f"{float(v):.{nd}f}"
    except Exception:
        return str(v)

doc = Document()
st = doc.styles["Normal"]; st.font.name = "Times New Roman"; st.font.size = Pt(12)

def omml(latexlike):
    return parse_xml(
        '<m:oMathPara xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">'
        f'<m:oMath><m:r><m:t>{latexlike}</m:t></m:r></m:oMath></m:oMathPara>')

def eq(text):
    p = doc.add_paragraph()
    p._p.append(omml(text))

# author-date citation helper: cite(p, "Baran and Wu, 1989")
def cite(par, text):
    par.add_run(f"({text})")

NCL = int(float(mv["sano_clusters"])+float(mv["kudamatsu_clusters"])+float(mv["yasu_clusters"]))
NFEAS = int(float(mv["sano_clusters_feasible"])+float(mv["kudamatsu_clusters_feasible"])+float(mv["yasu_clusters_feasible"]))
DEM = float(mv["sano_lv_demand_mw"])+float(mv["kudamatsu_lv_demand_mw"])+float(mv["yasu_lv_demand_mw"])

doc.add_heading("How Much Is Topology Flexibility Worth at Renewal? "
                "A Feasibility-Constrained Life-Cycle Assessment of LV "
                "Re-Layout During Undergrounding", 0)
doc.add_paragraph("Original research article prepared for Computer-Aided Civil "
                  "and Infrastructure Engineering (Wiley)")
doc.add_paragraph("[Authors and affiliations to be completed at submission]")
doc.add_paragraph("Corresponding author: [to be completed at submission]")

doc.add_heading("Abstract", 1)
doc.add_paragraph(
    "When aging overhead distribution lines are renewed by undergrounding, "
    "standard practice is like-for-like replacement along the existing "
    "route. Because the renewal window is the rare moment when topology can "
    "be re-chosen at committed civil cost, this study quantifies the value of "
    "topology flexibility (VoF) at renewal: the mean over legacy "
    "reconstruction replicates of max(0, NPC(replicate) − NPC(best feasible "
    "redesign)), a nonnegative estimand in which retaining the incumbent "
    "layout is an admissible decision. Re-layout is formulated as weighted "
    "Steiner-tree synthesis on the municipal road graph with per-edge "
    "conductor sizing, under explicit engineering feasibility gates (415 V "
    "radial feeders, coincident load, ~150 kVA transformer zones, ampacity, "
    "6% voltage-drop limit); the linearized power flow is AC-validated on "
    "every feasible synthesized feeder. Across "
    f"{NFEAS} feasible LV clusters serving {fmt(DEM,1)} MW of modeled demand "
    "in three Japanese municipalities, VoF is "
    f"{fmt(mv['sano_vof_pct'],2)}%, {fmt(mv['kudamatsu_vof_pct'],2)}%, and "
    f"{fmt(mv['yasu_vof_pct'],2)}% of like-for-like NPC — inside a "
    "prespecified 1% practical equivalence margin. A secondary naive "
    "contrast reaches −10%, but this is an estimand artifact, not a real "
    "saving. Once LV physics is respected, like-for-like renewal is a "
    "defensible default.")
doc.add_paragraph("Keywords: infrastructure renewal; distribution network "
                  "planning; undergrounding; Steiner tree; life-cycle cost; "
                  "engineering feasibility; open data")

doc.add_heading("1. Introduction", 1)
p = doc.add_paragraph(
    "Civil infrastructure systems face a large renewal cohort: aging "
    "overhead distribution lines are increasingly replaced by underground "
    "cables for resilience and amenity ")
cite(p, "Taheri et al., 2023")
p.add_run(". Renewal programs conventionally reproduce the legacy overhead "
    "route underground (like-for-like), because easements, customer drop "
    "points, and construction sequencing push planners toward the incumbent "
    "layout. Cost-benefit studies of undergrounding have evaluated the "
    "system-level policy choice of burying lines versus retaining overhead "
    "service ")
cite(p, "Fenrick and Getachew, 2012")
p.add_run("; ")
cite(p, "Larsen, 2016")
p.add_run(", and network-planning research has long treated topology as a "
    "decision variable at expansion, reconfiguration, or greenfield routing "
    "stages ")
cite(p, "Baran and Wu, 1989a")
p.add_run("; ")
cite(p, "Samui et al., 2012")
p.add_run("; ")
cite(p, "Camargo et al., 2013")
p.add_run("; ")
cite(p, "Kumar et al., 2014")
p.add_run(". However, the renewal window — when civil-works margins are "
    "already committed — is rarely examined as a topology decision point, "
    "and candidate designs are not always checked against LV electrical "
    "feasibility before cost comparison.")
p = doc.add_paragraph(
    "This paper contributes a feasibility-constrained method and a bounded "
    "empirical answer, not a case study of a particular municipality. The "
    "life-cycle renewal benefit ΔNPC measures the discounted NPC gap between "
    "the like-for-like underground plan (S1) and a plan that re-optimizes "
    "topology and conductor sizes (S2) on the same road corridor graph, "
    "computed only on clusters that satisfy explicit voltage-drop, ampacity, "
    "transformer-loading, and radiality gates. Because the true legacy "
    "topology is generally unobserved, we reconstruct it as an ensemble — "
    "in the spirit of data-driven geo-referenced LV topology synthesis ")
cite(p, "Abhilash et al., 2021")
p.add_run(" — and carry reconstruction uncertainty into the results via a "
    "topology divergence distance (TDD) rather than asserting a single "
    "ground truth. The optimization core uses a weighted Steiner-tree "
    "approximation ")
cite(p, "Kou et al., 1981")
p.add_run("; ")
cite(p, "Hwang and Richards, 1992")
p.add_run(" on the municipal road graph, with classical discretized "
    "conductor selection ")
cite(p, "Tram and Wall, 1988")
p.add_run(" and a linearized radial power-flow model ")
cite(p, "Baran and Wu, 1989b")
p.add_run("; ")
cite(p, "Gan and Low, 2014")
p.add_run(". Benchmark validation uses pandapower ")
cite(p, "Thurner et al., 2018")
p.add_run(". Demand geography derives from OpenStreetMap buildings and "
    "roads ")
cite(p, "Haklay and Weber, 2008")
p.add_run(", and a rooftop-PV extension follows distributed-generation "
    "planning practice ")
cite(p, "Tarraq et al., 2023")
p.add_run(". Asset-renewal context follows standard asset-management "
    "treatment of deteriorating infrastructure ")
cite(p, "Ross, 2019")
p.add_run(". The central methodological claim is that the *choice of "
    "estimand* determines whether re-layout appears valuable: a forced-"
    "redesign contrast manufactures apparent savings that vanish once the "
    "incumbent layout is admitted to the feasible design space.")

doc.add_heading("2. Data and methods", 1)
doc.add_heading("2.1 Study zones and data tiers", 2)
doc.add_paragraph(
    "Three municipalities were selected for complementary data tiers "
    "rather than representativeness of Japan as a whole (Table 1). Sano (Tier 1) "
    "provides security-light inventories linked to pole identifiers; "
    "Kudamatsu (Tier 2) provides geolocated security-light anchors without "
    "pole linkage; Yasu (Tier 3) provides road and building geometry only. "
    "Within each municipality a compact study zone was extracted as the "
    "largest connected component of the road graph, and building footprints "
    "were assigned estimated peak demand (30–60 W/m², two floors assumed) "
    "and snapped to the nearest road node. Buildings whose estimated raw "
    "peak exceeds 150 kW are marked medium-voltage-served and excluded from "
    "LV synthesis; this removes "
    f'{fmt(mv["sano_mv_demand_mw"],1)}, {fmt(mv["kudamatsu_mv_demand_mw"],1)}, and '
    f'{fmt(mv["yasu_mv_demand_mw"],1)} MW of modeled raw peak in the three '
    "zones respectively. All raw public data, checksums, and acquisition "
    "provenance are preserved in a machine-readable source registry.")
doc.add_heading("2.2 Feasibility-constrained reconstruction (S0)", 2)
doc.add_paragraph(
    "LV-served demand nodes are clustered into transformer zones of "
    "approximately 100 kW raw peak (the scale of a 150 kVA distribution "
    "transformer), and a coincidence factor of 0.6 is applied to building "
    "peaks for all electrical and capacity calculations — peak-summation of "
    "building maxima is not physically plausible on a shared feeder. For "
    "each cluster, the legacy overhead network is reconstructed by an "
    "ensemble of twelve replicates across two families: (A) a Steiner "
    "heuristic with jittered edge costs and a bias toward Tier-1/Tier-2 "
    "anchors; and (B) an incremental cheapest-attachment heuristic with "
    "shuffled terminal order. No replicate is claimed to be the true "
    "network. Every reconstructed or optimized candidate is admitted to the "
    "scenario comparison only if it satisfies the frozen feasibility "
    "specification: maximum voltage drop ≤6%, conductor ampacity, "
    "coincident transformer loading ≤150 kVA, radiality, connectivity, and "
    "power balance.")
doc.add_heading("2.3 Life-cycle cost model", 2)
doc.add_paragraph("For each candidate topology T the net present cost is")
eq("NPC(T) = CAPEX(T) + (E_loss(T)·p_e + CAPEX(T)·f_OM)·ADF(r, h)")
doc.add_paragraph(
    "where p_e is the electricity price, f_OM the annual O&M fraction, and "
    "ADF the annuity discount factor over horizon h=40 y at r=3%. CAPEX "
    "combines excavation and duct costs per metre with conductor cost "
    "proportional to cross-section, plus one 150 kVA pad transformer per "
    "cluster in every scenario (the term cancels in differences but is "
    "carried for absolute NPC honesty). Energy losses use the LinDistFlow "
    "quadratic expression")
eq("P_loss = Σ_e 3 I_e² R_e")
doc.add_paragraph(
    "scaled by a load factor of 0.35 to annual energy. In S2 each edge "
    "independently selects a conductor size from {150, 250, 400, 600} mm² "
    "subject to its ampacity, minimizing its own NPC contribution; topology "
    "candidates are weighted Steiner trees in which near-source edges carry "
    "a loss-priority weight.")
doc.add_paragraph(
    "Two contrasts are distinguished. The primary estimand is the value of "
    "topology flexibility")
eq("VoF = mean_r max(0, NPC(S1_r) − min(NPC(S1_r), NPC(S2)))")
doc.add_paragraph(
    "averaged over reconstruction replicates r: retaining the incumbent "
    "layout is an admissible decision inside the redesign set, so VoF is "
    "nonnegative by construction and measures the value of having redesign "
    "available as an option, not of forcing it. The secondary, naive "
    "contrast ΔNPC (defined below) instead compares the ensemble-based "
    "incumbent representation against a forced-redesign candidate set that "
    "excludes the incumbent itself. Economic equivalence is prespecified at "
    "|Δ|/NPC(S1) ≤ 1%: the margin was frozen before outcome inspection, "
    "derived from the model's resolution limits (±30% construction-cost "
    "uncertainty, surrogate loss-model error, and municipal unit-price "
    "variation), not from observed effect sizes.")
doc.add_heading("2.4 Scenarios and metrics", 2)
doc.add_paragraph(
    "S1 (like-for-like): each reconstruction replicate rebuilt underground "
    "with the reference 150 mm² conductor. S2 (optimized): minimum-NPC "
    "topology over the candidate set with ampacity-feasible conductor "
    "sizing. S3: S2 plus rooftop PV sized from clipped building footprints "
    "(30% usable roof, 0.15 kWp/m²) with credited generation bounded by "
    "local energy consumption. The primary metric is the life-cycle "
    "renewal benefit")
eq("ΔNPC = NPC(S1) − NPC(S2)")
doc.add_paragraph(
    "reported also as a percentage of NPC(S1). Topology divergence between "
    "the minimum-construction (w_loss=0) and the most loss-weighted "
    "candidate is measured by the topology divergence distance")
eq("TDD = 1 − |E_C ∩ E_L| / |E_C ∪ E_L|")
doc.add_paragraph(
    "over edge sets (an edge-set distance, not a likelihood). P(ΔNPC>0) "
    "from the Monte-Carlo driver sweep is reported only as model "
    "uncertainty, not as a claim about real-network behaviour.")

doc.add_heading("3. Results", 1)
doc.add_paragraph(
    f'Table 2 summarizes {NCL} clusters ({NFEAS} feasible) serving '
    f'{fmt(DEM,1)} MW of modeled LV peak demand — '
    f'{fmt(mv["sano_lv_share_total_pct"],0)}%, {fmt(mv["kudamatsu_lv_share_total_pct"],0)}%, '
    f'and {fmt(mv["yasu_lv_share_total_pct"],0)}% of total zone demand in '
    "Sano/Kudamatsu/Yasu (the remainder is MV-served by design and cancels "
    "in every contrast). The primary estimand VoF is "
    f'{fmt(mv["sano_vof_pct"],2)}% ({fmt(mv["sano_vof_bn"],4)} bn JPY), '
    f'{fmt(mv["kudamatsu_vof_pct"],2)}%, and {fmt(mv["yasu_vof_pct"],2)}%: '
    "all three zones fall inside the prespecified 1% economic-equivalence "
    "margin and are classified economically_equivalent. The secondary "
    "naive contrast ΔNPC is "
    f'{fmt(mv["sano_ltp_pct"],2)}%, {fmt(mv["kudamatsu_ltp_pct"],1)}%, and '
    f'{fmt(mv["yasu_ltp_pct"],2)}%; conductor upsizing is negligible and '
    "peak losses are essentially unchanged, so the contrast is entirely a "
    "construction-cost comparison (Figures 1–3).")
doc.add_paragraph(
    "Monte-Carlo sensitivity over discount rate (2–4.5%), electricity "
    "price (15–35 JPY/kWh), construction cost (±30%), O&M fraction, load "
    "factor, and horizon (30–50 y) yields P(ΔNPC>0) of "
    f'{fmt(mv["sano_mc_p_ltp_pos"],2)}, {fmt(mv["kudamatsu_mc_p_ltp_pos"],2)}, and '
    f'{fmt(mv["yasu_mc_p_ltp_pos"],2)}: Sano and Yasu are marginally but '
    "robustly positive, while Kudamatsu is robustly negative — its "
    "reconstructed legacy trees already sit near the cost optimum, so "
    "re-routing adds cable length without compensating loss savings "
    "(Figures 3–4). A secondary rooftop-PV overlay (S3; "
    f'{fmt(mv["sano_pv_mwp"],1)}, {fmt(mv["kudamatsu_pv_mwp"],1)}, and '
    f'{fmt(mv["yasu_pv_mwp"],1)} MWp modeled potential) is scenario-based, '
    "relies on generous self-consumption assumptions, and is reported as an "
    "upper bound in the Supplement (Figure S1); it does not alter the "
    "primary VoF conclusion.")

doc.add_heading("4. Discussion", 1)
p = doc.add_paragraph(
    "The central finding is bounded and informative: under the nonnegative "
    "VoF estimand, inherited LV layouts in all three zones are economically "
    "equivalent to the best feasible re-layout — the value of topology "
    "flexibility at renewal is below 0.5% of life-cycle cost everywhere. "
    "This sits alongside, and extends, two literatures that have not "
    "previously met. System-level cost-benefit analyses conclude that "
    "undergrounding is generally not cost-effective as a blanket policy ")
cite(p, "Fenrick and Getachew, 2012")
p.add_run("; ")
cite(p, "Larsen, 2016")
p.add_run("; our result shows that even inside a committed undergrounding "
    "program, the incumbent layout is already near the life-cycle optimum, "
    "so the residual value of re-layout is small. Feeder-routing and "
    "expansion-planning methods optimize topology against a fixed or "
    "greenfield demand surface ")
cite(p, "Samui et al., 2012")
p.add_run("; ")
cite(p, "Kumar et al., 2014")
p.add_run("; we add the renewal-window choice-set structure in which the "
    "incumbent remains admissible, turning the question from 'find the "
    "better network' into 'is the option to redesign worth exercising'. "
    "Geo-referenced synthesis of LV topologies from open data ")
cite(p, "Abhilash et al., 2021")
p.add_run(" provides the reconstruction precedent; we add feasibility "
    "gating and reconstruction-ensemble uncertainty before any cost "
    "contrast is drawn.")
doc.add_paragraph(
    "Two methodological controls produce the bounded result. First, "
    "feasibility gating: treating ~350 kW of raw building peaks as one "
    "undiversified LV load produces physically impossible feeders "
    "(double-digit voltage drops) and manufactures fictitious headroom. "
    "Second, estimand design: the negative Kudamatsu ΔNPC is an artifact "
    "of comparing an ensemble mean to candidate sets that exclude the "
    "incumbent; it is also not robust to the LV/MV boundary assumption "
    f'(moving the MV-served threshold to 200 kW flips Kudamatsu ΔNPC to '
    f'{fmt(mv["kudamatsu_dnpc_pct_mv200"],2)}%, and to 120 kW gives '
    f'{fmt(mv["kudamatsu_dnpc_pct_mv120"],2)}%). The mechanistic audit '
    "attributes it to a handful of small wide-area clusters where any "
    "rewiring costs 2–10× the incumbent corridor with no compensating "
    "loss reduction.")
p = doc.add_paragraph(
    "Limitations. Reconstructed topologies are modeled objects; even "
    "Tier-1 anchor data do not observe actual pole-to-pole routing, and "
    "results are conditional on the reconstruction ensemble (24-replicate "
    "and leave-one-family-out checks show stable estimates; S1 family "
    f'NPC ratios {fmt(mv["sano_fam_ratio"],3)}/{fmt(mv["kudamatsu_fam_ratio"],3)}/'
    f'{fmt(mv["yasu_fam_ratio"],3)}). The LinDistFlow surrogate was '
    "validated against pandapower AC power flow on all feasible "
    "synthesized feeders (max voltage-magnitude deviation "
    f'{fmt(mv["ac_vm_abs_max"],3)} pu, prespecified tolerance 0.02; '
    f'feasibility agreement {fmt(mv["ac_feas_agreement"],2)}; evaluated on '
    f'{fmt(mv["ac_n_feeders"],0)} feasible synthesized feeders, all '
    "converged). This validates the linearized calculations on "
    "synthesized feeder models, not actual municipal topology. "
    "Coincidence factor, demand densities, the 6% drop limit, and the "
    "150 kW LV/MV boundary are assumptions, not observations; the "
    "boundary assumption materially moves the ΔNPC contrast (Figure 4) "
    "though not the VoF ordering. MV-served demand is excluded by design "
    "and cancels in contrasts; the LV-modeled shares of total demand are "
    f'{fmt(mv["sano_lv_share_total_pct"],0)}%/{fmt(mv["kudamatsu_lv_share_total_pct"],0)}%/'
    f'{fmt(mv["yasu_lv_share_total_pct"],0)}%. Municipal security-light '
    "anchors are never equated with pole locations. Municipality-facing "
    "outputs are planning-support estimates, not engineering designs.")

doc.add_heading("5. Conclusions", 1)
doc.add_paragraph(
    "Under engineering-feasible LV reconstruction and a nonnegative "
    "value-of-flexibility estimand, renewal-time topology re-optimization "
    "is economically equivalent to like-for-like renewal in all three "
    f"study zones (VoF {fmt(mv['sano_vof_pct'],2)}–"
    f"{fmt(mv['kudamatsu_vof_pct'],2)}% of NPC, inside the prespecified "
    "1% margin). Large headline ΔNPC magnitudes reported for re-layout "
    "at renewal should be audited for feasibility gating and for estimand "
    "design before they are cited as benefits. For infrastructure asset "
    "management, the practical implication is that like-for-like "
    "undergrounding renewal is a defensible default at LV scale; the "
    "small modeled value of LV topology flexibility suggests that "
    "MV-level planning and distributed-generation integration may warrant "
    "separate evaluation rather than assuming substantial gains from LV "
    "re-layout alone.")

doc.add_heading("Acknowledgements", 1)
doc.add_paragraph("[to be completed at submission]")

doc.add_heading("Declarations", 1)
doc.add_paragraph("Declaration of generative AI: during the preparation of "
                  "this work the author used an AI coding assistant for "
                  "code scaffolding and drafting. The author reviewed and "
                  "edited all content and takes full responsibility for "
                  "the publication.")
doc.add_paragraph("Data availability: all scripts, the source registry, "
                  "checksums, and machine-readable result tables are "
                  "provided in the supplementary repository snapshot "
                  "(github.com/bougtoir/underground-topology). Municipal "
                  "open data were used under their stated licenses "
                  "(CC-BY for Kudamatsu).")
doc.add_paragraph("Conflict of interest: none declared. Funding: none.")

doc.add_heading("Figure captions (figures supplied as separate files)", 1)
for cap in [
    "Figure 1. Study zones: road graph (grey) and snapped building demand nodes (blue).",
    "Figure 2. Example feeder cluster: S1 like-for-like replicate vs S2 optimized layout.",
    "Figure 3. Primary estimand VoF (value of topology flexibility) by zone vs Monte-Carlo mean of the secondary naive ΔNPC.",
    "Figure 4. Sensitivity to engineering assumptions in all zones: secondary naive ΔNPC ranges (bars) vs primary VoF (dots); grey band = prespecified 1% economic-equivalence margin.",
]:
    doc.add_paragraph(cap)

doc.add_heading("Tables", 1)
doc.add_paragraph("Table 1. Study zones and data tiers")
t1 = doc.add_table(rows=4, cols=5); t1.style = "Table Grid"
hdr = ["Zone","Tier","LV demand (MW)","MV-excluded (MW)","Feasible clusters"]
for i, h in enumerate(hdr): t1.rows[0].cells[i].text = h
rows1 = [["Sano","1 (pole-ID linked)",fmt(mv["sano_lv_demand_mw"],1),fmt(mv["sano_mv_demand_mw"],1),str(int(float(mv["sano_clusters_feasible"])))],
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

doc.add_heading("References", 1)
REFS = [
 "Abhilash Bandam, Syranidou, C., Linssen, J. and Stolten, D. (2021). "
 "Geo-referenced synthetic low-voltage distribution networks: a "
 "data-driven approach. 2021 IEEE PES Innovative Smart Grid Technologies "
 "Europe (ISGT Europe), pp. 244–249. doi:10.1109/ISGTEurope52324.2021.9639916",
 "Baran, M.E. and Wu, F.F. (1989a). Network reconfiguration in "
 "distribution systems for loss reduction and load balancing. IEEE "
 "Transactions on Power Delivery 4(2): 1401–1407. doi:10.1109/61.25627",
 "Baran, M.E. and Wu, F.F. (1989b). Optimal capacitor placement on "
 "radial distribution systems. IEEE Transactions on Power Delivery "
 "4(1): 725–734. doi:10.1109/61.19265",
 "Camargo, V., Lavorato, M. and Romero, R. (2013). Specialized genetic "
 "algorithm to solve the electrical distribution system expansion "
 "planning. 2013 IEEE Power & Energy Society General Meeting, pp. 1–5. "
 "doi:10.1109/PESMG.2013.6672615",
 "Fenrick, S.A. and Getachew, L. (2012). Cost and reliability "
 "comparisons of underground and overhead power lines. Utilities Policy "
 "20(1): 31–37. doi:10.1016/j.jup.2011.10.002",
 "Gan, L. and Low, S.H. (2014). Convex relaxations and linear "
 "approximation for optimal power flow in multiphase radial networks. "
 "2014 Power Systems Computation Conference, pp. 1–9. "
 "doi:10.1109/PSCC.2014.7038399",
 "Haklay, M. and Weber, P. (2008). OpenStreetMap: user-generated street "
 "maps. IEEE Pervasive Computing 7(4): 12–18. doi:10.1109/MPRV.2008.80",
 "Hwang, F.K. and Richards, D.S. (1992). Steiner tree problems. "
 "Networks 22(1): 55–89. doi:10.1002/net.3230220105",
 "Kou, L., Markowsky, G. and Berman, L. (1981). A fast algorithm for "
 "Steiner trees. Acta Informatica 15(2): 141–145. doi:10.1007/BF00288961",
 "Kumar, D., Samantaray, S.R. and Joos, G. (2014). A reliability "
 "assessment based graph theoretical approach for feeder routing in "
 "power distribution networks including distributed generations. "
 "International Journal of Electrical Power & Energy Systems 57: 11–30. "
 "doi:10.1016/j.ijepes.2013.11.039",
 "Larsen, P.H. (2016). A method to estimate the costs and benefits of "
 "undergrounding electricity transmission and distribution lines. "
 "Energy Economics 60: 47–61. doi:10.1016/j.eneco.2016.09.011",
 "Ross, R. (2019). Reliability Analysis for Asset Management of "
 "Electric Power Grids. Wiley. doi:10.1002/9781119125204",
 "Samui, A., Singh, S., Ghose, T. and Samantaray, S.R. (2012). A direct "
 "approach to optimal feeder routing for radial distribution system. "
 "IEEE Transactions on Power Delivery 27(1): 253–260. "
 "doi:10.1109/TPWRD.2011.2167522",
 "Taheri, B., Molzahn, D.K. and Grijalva, S. (2023). Improving "
 "distribution system resilience by undergrounding lines and deploying "
 "mobile generators. Electric Power Systems Research 214: 108804. "
 "doi:10.1016/j.epsr.2022.108804",
 "Tarraq, A., Mariami, F.E., Belfqih, A. and Haidi, T. (2023). Optimal "
 "renewable distributed generation planning: an up-to-date "
 "state-of-the-art review. International Journal of Global Energy "
 "Issues 45(4/5): 315–348. doi:10.1504/IJGEI.2023.132011",
 "Thurner, L., Scheidler, A., Schafer, F., Menke, J.-H., Dollichon, J., "
 "Meier, F., Meinecke, S. and Braun, M. (2018). Pandapower — an "
 "open-source Python tool for convenient modeling, analysis, and "
 "optimization of electric power systems. IEEE Transactions on Power "
 "Systems 33(6): 6510–6521. doi:10.1109/TPWRS.2018.2829021",
 "Tram, H.N. and Wall, D.L. (1988). Optimal conductor selection in "
 "planning radial distribution systems. IEEE Transactions on Power "
 "Systems 3(1): 200–206. doi:10.1109/59.43199",
]
for r in REFS:
    doc.add_paragraph(r)

out = f"{ROOT}/manuscript/manuscript_caie_v1.docx"
doc.save(out)
print("saved", out, "| refs:", len(REFS))

