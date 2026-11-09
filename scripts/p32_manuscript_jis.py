"""Build JIS_submission/JIS_MANUSCRIPT_FINAL.docx in ASCE Journal of Infrastructure
Systems layout (unnumbered headings, abstract + Practical Applications, author-date
references, figure captions then tables at the end, figures supplied separately).
Every number is read from analysis/, data/processed/ and config/ outputs."""
import os, re, sys, yaml
import pandas as pd
import docx
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_LINE_SPACING, WD_BREAK, WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement, parse_xml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = f"{ROOT}/analysis"
OUT = f"{ROOT}/JIS_submission/JIS_MANUSCRIPT_FINAL.docx"
Z = ["sano", "kudamatsu", "yasu"]
ZN = {"sano": "Sano", "kudamatsu": "Kudamatsu", "yasu": "Yasu"}

# ---------------------------------------------------------------- numbers
sr = pd.read_csv(f"{A}/scenario_results_v2.csv").set_index("city")
rc = {z: pd.read_csv(f"{ROOT}/data/processed/{z}/cluster_results_v2.csv") for z in Z}
fe = {z: r[r.s2_feasible & (r.n_s1_feas > 0)] for z, r in rc.items()}
zm = pd.read_csv(f"{A}/CEUS_ZERO_MASS_SUMMARY.csv").set_index("city")
ac0 = pd.read_csv(f"{A}/AC_VS_LINEAR_VALIDATION.csv")
ac1 = pd.read_csv(f"{A}/JIS_AC_CLUSTERLOAD_CHECK.csv")
eng = pd.read_csv(f"{A}/ENGINEERING_ASSUMPTION_SENSITIVITY.csv")
mor = pd.read_csv(f"{A}/MORPHOLOGY_CORRELATIONS_CORRECTED.csv").set_index("predictor")
spd = pd.read_csv(f"{A}/CEUS_SPATIAL_DIAGNOSTICS.csv").set_index("city")
mc = pd.read_csv(f"{A}/sensitivity_mc_v2.csv").set_index("city")
cfg = yaml.safe_load(open(f"{ROOT}/config/study.yaml"))
spec = yaml.safe_load(open(f"{ROOT}/config/ENGINEERING_FEASIBILITY_SPEC.yaml"))
eqs = yaml.safe_load(open(f"{ROOT}/config/ECONOMIC_EQUIVALENCE_SPEC.yaml"))

def find_margin(d):
    if isinstance(d, dict):
        for k, v in d.items():
            if "margin" in str(k).lower() and isinstance(v, (int, float)):
                return float(v)
            m = find_margin(v)
            if m is not None:
                return m
    return None
MARGIN = find_margin(eqs); MARGIN = MARGIN * 100 if MARGIN < 0.5 else MARGIN
POS_TOL = 1e-6

N_all = sum(len(r) for r in rc.values())
N_f = {z: len(f) for z, f in fe.items()}; NF = sum(N_f.values())
N_nt = {z: int((f.terminals > 1).sum()) for z, f in fe.items()}; NNT = sum(N_nt.values())
N_pos = {z: int(((100 * f.vof_mean / f.s1_npc_feas_mean) > POS_TOL).sum()) for z, f in fe.items()}
NPOS = sum(N_pos.values())
assert all(N_pos[z] == zm.loc[z, "positive_vof"] for z in Z)
MW_all = sum(r.raw_kw.sum() for r in rc.values()) / 1e3
MW_f = sum(f.raw_kw.sum() for f in fe.values()) / 1e3
VOF = {z: sr.loc[z, "vof_pct"] for z in Z}
VOF_NT = {z: 100 * fe[z][fe[z].terminals > 1].vof_mean.sum() / fe[z][fe[z].terminals > 1].s1_npc_feas_mean.sum() for z in Z}
MAXC = {z: zm.loc[z, "max_vof_pct"] for z in Z}
MEDC = {z: zm.loc[z, "median_vof_pct_given_positive"] for z in Z}
NAIVE_K = sr.loc["kudamatsu", "ltp_pct"]
ev = eng[eng.parameter != "baseline"]
N_VAR = len(ev) // 3
assert N_VAR * 3 == len(ev)
VMIN, VMAX = ev.vof_pct.min(), ev.vof_pct.max()
VDMAX_ENG = ev.max_vdrop.max()
MC_K5, MC_K95 = mc.loc["kudamatsu", "delta_p5"] / 1e9, mc.loc["kudamatsu", "delta_p95"] / 1e9
N_MC = int(mc.loc["kudamatsu", "n_draws"])
VDMAX = max(max(f.s1_vdrop_max.max(), f.s2_vdrop.max()) for f in fe.values())
SINGLE = NF - NNT

def acstats(d):
    return dict(n=len(d), cl=d.groupby(["city", "cluster"]).ngroups, nc=int((~d.converged.astype(bool)).sum()),
                agree=(d.feas_lin == d.feas_ac).mean(), both=int((d.feas_lin & d.feas_ac).sum()),
                dvmax=d.vm_abs_err.max(), dvmed=d.vm_abs_err.median(), lmax=d.loss_rel_err.max(),
                lin=d.lin_vdrop_pct.max(), ac=d.ac_vdrop_pct.max())
AC1, AC0 = acstats(ac1), acstats(ac0)
H = cfg["project"]["primary_horizon_years"]; DR = cfg["project"]["discount_rate"] * 100
EK = cfg["cost_model"]["electricity_jpy_per_kwh"]; OMF = cfg["cost_model"]["om_fraction_of_capex"] * 100
LF = cfg["project"]["load_factor"]
EXC = cfg["cost_model"]["excavation_jpy_per_m"]; DUCT = cfg["cost_model"]["duct_bank_jpy_per_m"]
CAB = cfg["cost_model"]["cable_lv_jpy_per_m"]; XF = spec["feasibility"]["transformer"]["unit_cost_jpy"]
VD = spec["feasibility"]["voltage_drop_max_pct"]; KVA = spec["feasibility"]["transformer"]["rated_kva"]
CF = spec["demand_model"]["coincidence_factor"]; VLL = spec["power_flow"]["v_ll_v"]; PF = spec["power_flow"]["power_factor"]
AMP = spec["feasibility"]["ampacity_a"]; SIZES = spec["feasibility"]["conductor_sizes_mm2"]
RHO = spec["power_flow"]["rho_ohm_m"]
RHO_S = morx = None
def rho(p, col="spearman_rho_pooled"): return mor.loc[p, col]
MORAN = (spd.moran_i.min(), spd.moran_i.max()); MORAN_P = spd.perm_p_value.min()

def p2(x): return f"{x:.2f}"
def pct(x, d=2): return f"{x:.{d}f}%"
def n(x): return f"{x:,}"

# ---------------------------------------------------------------- references
REFS = {
 "Abdel-Mottaleb and Zhang 2020": 'Abdel-Mottaleb, N., and Q. Zhang. 2020. "Water distribution–transportation interface connectivity responding to urban geospatial morphology." J. Infrastruct. Syst. 26 (3): 04020025. https://doi.org/10.1061/(ASCE)IS.1943-555X.0000563.',
 "Abu-Samra et al. 2020": 'Abu-Samra, S., M. Ahmed, and L. Amador. 2020. "Asset management framework for integrated municipal infrastructure." J. Infrastruct. Syst. 26 (4): 04020039. https://doi.org/10.1061/(ASCE)IS.1943-555X.0000580.',
 "Babli et al. 2025": 'Babli, M., T. Gebhard, and E. Brucherseifer. 2025. "Open data-driven reconstruction of power distribution grid: A land use-based approach." Electronics 14 (7): 1414. https://doi.org/10.3390/electronics14071414.',
 "Bandam et al. 2021": 'Bandam, A., C. Syranidou, J. Linssen, and D. Stolten. 2021. "Geo-referenced synthetic low-voltage distribution networks: A data-driven approach." In Proc., 2021 IEEE PES Innovative Smart Grid Technologies Europe (ISGT Europe), 1–6. New York: IEEE. https://doi.org/10.1109/ISGTEurope52324.2021.9639916.',
 "Baran and Wu 1989": 'Baran, M. E., and F. F. Wu. 1989. "Network reconfiguration in distribution systems for loss reduction and load balancing." IEEE Trans. Power Delivery 4 (2): 1401–1407. https://doi.org/10.1109/61.25627.',
 "Basupi and Kapelan 2015": 'Basupi, I., and Z. Kapelan. 2015. "Evaluating flexibility in water distribution system design under future demand uncertainty." J. Infrastruct. Syst. 21 (2): 04014034. https://doi.org/10.1061/(ASCE)IS.1943-555X.0000199.',
 "Boeing 2020": 'Boeing, G. 2020. "A multi-scale analysis of 27,000 urban street networks: Every US city, town, urbanized area, and Zillow neighborhood." Environ. Plann. B: Urban Anal. City Sci. 47 (4): 590–608. https://doi.org/10.1177/2399808318784595.',
 "Bynum et al. 2021": 'Bynum, M., A. Staid, B. Arguello, A. Castillo, B. Knueven, C. D. Laird, and J.-P. Watson. 2021. "Proactive operations and investment planning via stochastic optimization to enhance power systems\' extreme weather resilience." J. Infrastruct. Syst. 27 (2): 04021004. https://doi.org/10.1061/(ASCE)IS.1943-555X.0000603.',
 "Cardillo et al. 2006": 'Cardillo, A., S. Scellato, V. Latora, and S. Porta. 2006. "Structural properties of planar graphs of urban street patterns." Phys. Rev. E 73 (6): 066107. https://doi.org/10.1103/PhysRevE.73.066107.',
 "Chahinian et al. 2019": 'Chahinian, N., C. Delenne, B. Commandré, M. Derras, L. Deruelle, and J.-S. Bailly. 2019. "Automatic mapping of urban wastewater networks based on manhole cover locations." Comput. Environ. Urban Syst. 78: 101370. https://doi.org/10.1016/j.compenvurbsys.2019.101370.',
 "Dao et al. 2019": 'Dao, C. D., A. Hartmann, A. Lamper, and P. Herbert. 2019. "Scheduling infrastructure renewal for railway networks." J. Infrastruct. Syst. 25 (4): 04019027. https://doi.org/10.1061/(ASCE)IS.1943-555X.0000515.',
 "Dehghani et al. 2025": 'Dehghani, M. S., Y. Y. Kesete, and S. McNeil. 2025. "Assembling the data to support risk-based asset management: A case study of Dominica\'s roadway network." J. Infrastruct. Syst. 31 (2): 05025001. https://doi.org/10.1061/JITSE4.ISENG-2459.',
 "Fenrick and Getachew 2012": 'Fenrick, S. A., and L. Getachew. 2012. "Cost and reliability comparisons of underground and overhead power lines." Util. Policy 20 (1): 31–37. https://doi.org/10.1016/j.jup.2011.10.002.',
 "Fletcher et al. 2026": 'Fletcher, S., M. Chester, K. Klise, R. Jain, I. Searles, R. Sparks, R. Hoff, K. Bonney, S. Rivera, and J. Poff. 2026. "Challenges and opportunities for synthetic water distribution models." J. Infrastruct. Syst. 32 (4): 05026007. https://doi.org/10.1061/JITSE4.ISENG-3052.',
 "Gan and Low 2014": 'Gan, L., and S. H. Low. 2014. "Convex relaxations and linear approximation for optimal power flow in multiphase radial networks." In Proc., 2014 Power Systems Computation Conf., 1–9. New York: IEEE. https://doi.org/10.1109/PSCC.2014.7038399.',
 "Gilbert et al. 2021": 'Gilbert, T., P. James, L. Smith, S. Barr, and J. Morley. 2021. "Topological integration of BIM and geospatial water utility networks across the building envelope." Comput. Environ. Urban Syst. 86: 101570. https://doi.org/10.1016/j.compenvurbsys.2020.101570.',
 "Hadzilacos et al. 2000": 'Hadzilacos, T., D. Kalles, N. Preston, P. Melbourne, L. Camarinopoulos, M. Eimermacher, V. Kallidromitis, S. Frondistou-Yannas, and S. Saegrov. 2000. "UtilNets: A water mains rehabilitation decision-support system." Comput. Environ. Urban Syst. 24 (3): 215–232. https://doi.org/10.1016/S0198-9715(99)00058-7.',
 "Haklay and Weber 2008": 'Haklay, M., and P. Weber. 2008. "OpenStreetMap: User-generated street maps." IEEE Pervasive Comput. 7 (4): 12–18. https://doi.org/10.1109/MPRV.2008.80.',
 "Hastak and Gokhale 2000": 'Hastak, M., and S. Gokhale. 2000. "System for evaluating underground pipeline renewal options." J. Infrastruct. Syst. 6 (3): 105–113. https://doi.org/10.1061/(ASCE)1076-0342(2000)6:3(105).',
 "Kerwin and Adey 2021": 'Kerwin, S., and B. T. Adey. 2021. "Integrated planning of operational maintenance programs for water and gas distribution networks." J. Infrastruct. Syst. 27 (4): 04021039. https://doi.org/10.1061/(ASCE)IS.1943-555X.0000646.',
 "Khan et al. 2015": 'Khan, Z., O. Moselhi, and T. Zayed. 2015. "Identifying rehabilitation options for optimum improvement in municipal asset condition." J. Infrastruct. Syst. 21 (2): 04014037. https://doi.org/10.1061/(ASCE)IS.1943-555X.0000220.',
 "Kou et al. 1981": 'Kou, L., G. Markowsky, and L. Berman. 1981. "A fast algorithm for Steiner trees." Acta Inf. 15 (2): 141–145. https://doi.org/10.1007/BF00288961.',
 "Kudamatsu City n.d.": 'Kudamatsu City. n.d. "Security-light inventory [in Japanese]." Yamaguchi Open Data Catalog. Accessed September 24, 2026. https://yamaguchi-opendata.jp/ckan/dataset/cbc4f005-7812-41f6-8f5a-b9ed044a4f81.',
 "Kumar et al. 2014": 'Kumar, D., S. R. Samantaray, and G. Joos. 2014. "A reliability assessment based graph theoretical approach for feeder routing in power distribution networks including distributed generations." Int. J. Electr. Power Energy Syst. 57: 11–30. https://doi.org/10.1016/j.ijepes.2013.11.039.',
 "Larsen 2016": 'Larsen, P. H. 2016. "A method to estimate the costs and benefits of undergrounding electricity transmission and distribution lines." Energy Econ. 60: 47–61. https://doi.org/10.1016/j.eneco.2016.09.011.',
 "Leo and Swei 2021": 'Leo, B., and O. Swei. 2021. "Life-cycle cost analysis framework to support data procurement strategies for infrastructure assets." J. Infrastruct. Syst. 27 (1): 05020011. https://doi.org/10.1061/(ASCE)IS.1943-555X.0000596.',
 "Liu et al. 2025": 'Liu, D., J. S. Giraldo, P. Palensky, and P. P. Vergara. 2025. "Topology identification and parameters estimation of LV distribution networks using open GIS data." Int. J. Electr. Power Energy Syst. 164: 110395. https://doi.org/10.1016/j.ijepes.2024.110395.',
 "Moghtadernejad et al. 2023": 'Moghtadernejad, S., Y. Jin, and B. T. Adey. 2023. "Estimating the values of missing data related to infrastructure condition states using their spatial correlation." J. Infrastruct. Syst. 29 (1): 04022041. https://doi.org/10.1061/(ASCE)IS.1943-555X.0000726.',
 "Natural Earth n.d.": 'Natural Earth. n.d. "1:10m physical vectors: Land." Accessed September 24, 2026. https://www.naturalearthdata.com/downloads/10m-physical-vectors/.',
 "Onishi 2026": 'Onishi, T. 2026. "underground-topology: Code, configuration, and generated results for feasibility-gated renewal reconfiguration screening." GitHub. Accessed November 9, 2026. https://github.com/bougtoir/underground-topology.',
 "OpenStreetMap Contributors 2026": 'OpenStreetMap Contributors. 2026. "OpenStreetMap road and building data, retrieved via the Overpass API." Accessed September 24, 2026. https://www.openstreetmap.org.',
 "Runfola et al. 2020": 'Runfola, D., et al. 2020. "geoBoundaries: A global database of political administrative boundaries." PLoS One 15 (4): e0231866. https://doi.org/10.1371/journal.pone.0231866.',
 "Salman and Li 2017": 'Salman, A. M., and Y. Li. 2017. "Assessing climate change impact on system reliability of power distribution systems subjected to hurricanes." J. Infrastruct. Syst. 23 (1): 04016024. https://doi.org/10.1061/(ASCE)IS.1943-555X.0000316.',
 "Samui et al. 2012": 'Samui, A., S. Singh, T. Ghose, and S. R. Samantaray. 2012. "A direct approach to optimal feeder routing for radial distribution system." IEEE Trans. Power Delivery 27 (1): 253–260. https://doi.org/10.1109/TPWRD.2011.2167522.',
 "Sano City n.d.": 'Sano City. n.d. "Security-light data [in Japanese]." Accessed September 24, 2026. https://www.city.sano.lg.jp/material/files/group/17/100.csv.',
 "Taheri et al. 2023": 'Taheri, B., D. K. Molzahn, and S. Grijalva. 2023. "Improving distribution system resilience by undergrounding lines and deploying mobile generators." Electr. Power Syst. Res. 214: 108804. https://doi.org/10.1016/j.epsr.2022.108804.',
 "Thurner et al. 2018": 'Thurner, L., A. Scheidler, F. Schafer, J.-H. Menke, J. Dollichon, F. Meier, S. Meinecke, and M. Braun. 2018. "Pandapower—An open-source Python tool for convenient modeling, analysis, and optimization of electric power systems." IEEE Trans. Power Syst. 33 (6): 6510–6521. https://doi.org/10.1109/TPWRS.2018.2829021.',
 "Tram and Wall 1988": 'Tram, H. N., and D. L. Wall. 1988. "Optimal conductor selection in planning radial distribution systems." IEEE Trans. Power Syst. 3 (1): 200–206. https://doi.org/10.1109/59.43199.',
 "Zahed et al. 2020": 'Zahed, S. E., S. M. Shahandashti, and J. D. Diltz. 2020. "Investment valuation of underground freight transportation systems under uncertainty." J. Infrastruct. Syst. 26 (3): 04020029. https://doi.org/10.1061/(ASCE)IS.1943-555X.0000568.',
 "Zhang et al. 2025": 'Zhang, F., Z. Xu, R. Zhu, C. Liang, and D. Gu. 2025. "Geospatial mapping of urban utility networks integrating street view images and design rules." Comput.-Aided Civ. Infrastruct. Eng. 40 (27): 4884–4903. https://doi.org/10.1111/mice.70085.',
}

# ---------------------------------------------------------------- text
TITLE = ("Is Network Reconfiguration Worth It at Infrastructure Renewal? A Feasibility-Gated "
         "Economic Screening of Low-Voltage Distribution Re-Layout during Undergrounding")
AUTHOR = "Tatsuki Onishi"
AFFIL = ("[Author title, affiliation, and full postal address to be entered by the author before submission]. "
         "Email: [corresponding-author email].")

WORDS = {i: w for i, w in enumerate("zero one two three four five six seven eight nine".split())}
vz = f"{p2(VOF['sano'])}%, {p2(VOF['kudamatsu'])}%, and {p2(VOF['yasu'])}%"
ABSTRACT = (
 "Scheduled renewal of urban infrastructure, such as the conversion of overhead electricity distribution lines to "
 "underground cable, commits civil works that could also be used to reconfigure the network. Whether such "
 "reconfiguration is worth undertaking is rarely evaluated directly: optimization studies usually compare a "
 "redesigned network with a greenfield or forced alternative rather than with retention of the existing layout, and "
 "the existing layout is often only partially recorded. This study develops a feasibility-gated screening method "
 "that estimates the economic value of reconfiguration at renewal while keeping like-for-like replacement as an "
 "admissible option. Incumbent low-voltage networks were reconstructed as ensembles from open municipal records "
 "and OpenStreetMap data in three Japanese study zones with different levels of record observability. Candidate "
 "redesigns were generated as weighted Steiner trees on the road network and admitted only if they satisfied "
 "radiality, coincident-peak ampacity, transformer-capacity, and voltage-drop limits; their life-cycle net present "
 "cost was then compared with that of the reconstructed incumbent. Of "
 f"{n(N_all)} transformer-zone clusters, {n(NF)} were electrically feasible. The value of reconfiguration was "
 f"{vz} of like-for-like life-cycle cost in the three zones, all within a prespecified {MARGIN:.0f}% "
 f"practical-equivalence margin, and it stayed below {MARGIN:.0f}% under {WORDS.get(N_VAR, N_VAR)} alternative engineering "
 f"assumptions. Value was positive in only {NPOS} clusters, reaching at most {max(MAXC.values()):.1f}% in a single "
 "cluster, and its apparent association with urban form reduced to cluster size. Full alternating-current power-flow "
 f"checks agreed with the linear feasibility screen for all {n(AC1['n'])} feeder–scenario cases. Under these "
 "reconstructed conditions, like-for-like renewal is a defensible default, and the method is best used to identify "
 "the small set of renewal sites where detailed reconfiguration engineering may be justified.")

PRACTICAL = (
 "When a city replaces overhead power lines with underground cables, the excavation needed for the new ducts also "
 "creates an opportunity to change how the local low-voltage network is laid out. Planners often assume that a "
 "redesigned layout should be cheaper or better. This study tests that assumption in three Japanese districts. Public "
 "data were used to approximate the existing network, engineering checks ensured that every alternative could carry "
 "the load within voltage and equipment limits, and life-cycle cost was used to compare alternatives. Keeping the "
 "existing layout was always allowed as an option. In most transformer zones, no feasible redesign was cheaper than "
 "replacing the existing layout like for like, and in each district the potential saving was below "
 f"{max(VOF.values()):.1f}% of life-cycle cost. A few larger zones showed savings of several percent. The practical "
 "implication for utilities and municipalities is that renewal programs need not commission detailed redesign "
 "studies everywhere. A low-cost screening step can flag the few locations where redesign may pay, and these "
 "locations should then be checked with actual utility records and detailed engineering before any investment "
 "decision is made.")

S = []  # (kind, text)
def h1(t): S.append(("h1", t))
def h2(t): S.append(("h2", t))
def para(t): S.append(("p", t))
def eq(key): S.append(("eq", key))

h1("Introduction")
para("Much of the civil infrastructure that serves cities is approaching the end of its design life, and renewal "
     "programs for water, gas, transport, and electricity networks commit large public and private budgets to "
     "replacing aging assets (Abu-Samra et al. 2020; Kerwin and Adey 2021). Renewal decisions are usually framed as "
     "asset-level questions of when and how to replace components (Hadzilacos et al. 2000; Hastak and Gokhale 2000; Khan et al. 2015) or as "
     "network-level scheduling problems that coordinate interventions across interdependent assets (Dao et al. 2019). "
     "A scheduled renewal also creates a less frequently examined opportunity: because excavation, duct installation, "
     "and reinstatement are paid for anyway, the renewal window is a rare moment at which the spatial configuration "
     "of a buried network can be changed at marginal rather than full cost.")
para("The conversion of overhead electricity distribution to underground cable is a clear example. Undergrounding "
     "programs are justified mainly by resilience, safety, and streetscape objectives, and economic studies show that "
     "blanket undergrounding rarely passes a cost–benefit test while targeted undergrounding can (Fenrick and Getachew "
     "2012; Larsen 2016; Taheri et al. 2023). Long-horizon studies of power distribution reliability likewise treat "
     "undergrounding as an infrastructure investment strategy (Salman and Li 2017). Once a corridor has been committed "
     "to undergrounding, however, a narrower marginal question remains for the low-voltage network: should the "
     "inherited layout be replaced like for like, or should the committed civil works be used to re-lay the network "
     "along a different, possibly shorter or lower-loss, topology?")
para("A technically feasible redesign is not necessarily an economically justified one. Distribution-planning "
     "methods have long optimized feeder routing, conductor selection, and reconfiguration (Tram and Wall 1988; Baran "
     "and Wu 1989; Samui et al. 2012; Kumar et al. 2014), and recent infrastructure-systems work optimizes "
     "power-network investment under engineering constraints (Bynum et al. 2021). These formulations typically "
     "compare an optimized network with a greenfield design or with a forced alternative. When the comparison "
     "excludes the incumbent configuration, any redesign that is feasible will appear to offer some saving or some "
     "loss, and the reported difference conflates genuine decision value with the arbitrary choice of comparator. The "
     "relevant renewal question is different: the incumbent layout remains an admissible decision, and a redesign has "
     "value only to the extent that it improves on that default.")
para("This framing has a direct analogue in the infrastructure-systems literature on flexibility. Flexibility in "
     "network design has been valued as the cost difference between adaptable and committed plans (Basupi and "
     "Kapelan 2015), adaptive planning pathways have been proposed to avoid costly redesigns (Hadjidemetriou et al. "
     "2022), and real-options methods have been used to value underground infrastructure investment under "
     "uncertainty (Zahed et al. 2020). The present study applies the same logic to a one-shot decision at renewal: "
     "the option to reconfigure is valued against the option to retain. Because the incumbent is always admissible, "
     "this value cannot be negative; its non-negativity is a property of the decision formulation, not an empirical "
     "finding. The empirical questions are how large the value is, how it is distributed across the network, and "
     "whether it is large enough relative to modeling uncertainty to justify detailed engineering.")
para("A second difficulty is that the incumbent configuration is often poorly recorded. Infrastructure managers "
     "routinely make decisions with incomplete or missing asset data (Moghtadernejad et al. 2023; Dehghani et al. "
     "2025), and the value of acquiring better data can itself be evaluated as a life-cycle cost decision (Leo and "
     "Swei 2021). For buried utility networks, synthetic or reconstructed models built from road networks and other "
     "proxies are increasingly used where utility records are unavailable (Bandam et al. 2021; Zhang et al. 2025; "
     "Liu et al. 2025; Babli et al. 2025), and their fidelity limits have been documented against ground truth "
     "(Fletcher et al. 2026). Utility networks are known to follow the morphology of the street network "
     "(Abdel-Mottaleb and Zhang 2020). "
     "Reconstruction therefore offers a way to screen renewal decisions before detailed records are assembled, "
     "provided that its uncertainty is carried through to the decision and its conditionality is stated.")
para("This paper develops and applies a feasibility-gated screening method for renewal-time reconfiguration of "
     "low-voltage distribution networks during undergrounding. Incumbent networks are reconstructed as ensembles from "
     "open data in three Japanese study zones that differ in record observability; candidate redesigns are generated "
     "on the road network; every alternative, including the incumbent, must pass explicit engineering feasibility "
     "gates before any cost comparison; and the value of reconfiguration is defined as the expected life-cycle cost "
     "saving of the best feasible redesign relative to an admissible incumbent. The study asks three questions: (1) how "
     "large is the economic value of reconfiguration at renewal once feasibility and the incumbent option are "
     "respected; (2) where, if anywhere, is that value concentrated; and (3) how robust are these conclusions to "
     "engineering, economic, and electrical-model assumptions. The contribution is not a new optimization algorithm. "
     "It is a decision estimand and screening procedure for infrastructure renewal, together with evidence on the "
     "size and distribution of that value under reconstructed-network conditions (Fig. 1).")

h1("Methods")
h2("Study Design and Zones")
para("Three Japanese municipalities were selected purposively for the availability of public spatial data relevant "
     "to reconstructing low-voltage network layouts, not to represent Japanese municipalities statistically (Table 1). "
     "Sano (Tochigi Prefecture) publishes security-light records with pole numbers and coordinates (observability "
     "tier 1; Sano City n.d.); Kudamatsu (Yamaguchi Prefecture) publishes geolocated security-light records without "
     "verified pole linkage (tier 2; Kudamatsu City n.d.); and Yasu (Shiga Prefecture) is represented by road and "
     "building geometry only (tier 3). In each municipality a "
     "compact study zone was extracted as the largest connected component of the OpenStreetMap road graph (Haklay and "
     "Weber 2008; OpenStreetMap Contributors 2026) (Fig. 2). Building footprints were assigned an estimated peak "
     "demand of 30–60 W/m² over two floors and snapped to the nearest road node; mean snap distances of 37–49 m are "
     "treated as error in the modeled demand surface. Buildings whose raw peak exceeded "
     f"{spec['demand_model'].get('lv_max_node_kw', 150)} kW were treated as served at medium voltage and excluded "
     "from low-voltage synthesis. Demand nodes were grouped into transformer-zone clusters, which are the unit of "
     "decision and analysis.")
h2("Reconstruction of Incumbent Networks")
para("Because actual low-voltage cable routes are unobserved, each cluster's incumbent network was reconstructed as "
     "an ensemble of radial trees on the road graph, which serves as the admissible conduit space. Security-light "
     "anchors, where available, were used as routing priors on the demand side and were never equated with pole or "
     "cable locations, unlike approaches that treat surface features as network nodes (Chahinian et al. 2019). The "
     "evidence available in each tier determined how strongly the reconstruction was constrained, following the "
     "logic of integration under incomplete semantics (Gilbert et al. 2021). The primary ensemble comprises 12 "
     "replicates per cluster drawn from two generator families; a 24-replicate ensemble and leave-one-family-out "
     "variants were used to check stability. The incumbent was evaluated with the 150 mm² reference conductor "
     "throughout, representing like-for-like replacement of the inherited configuration.")
h2("Candidate Redesigns")
para("Redesign candidates were generated for each cluster as weighted Steiner trees connecting the transformer "
     "source and all demand terminals on the local road graph, using the Kou–Markowsky–Berman heuristic (Kou et al. "
     "1981). Edge weights combined route length with a load-dependent loss penalty, and six "
     "penalty weights (0, 1, 3, 10, 30, and 100) produced a family of candidates ranging from minimum-length to "
     "loss-averse trees. Each candidate tree was pruned to its terminals, and conductor sizes were selected edge by "
     f"edge from {', '.join(str(s) for s in SIZES)} mm² to minimize capital plus discounted loss cost subject to "
     "ampacity. The best redesign is therefore the least-cost member of an enumerated candidate set, not a proven "
     "optimum over all possible layouts; the resulting value is a lower bound on what an exhaustive search could "
     "find under the same model.")
h2("Engineering Feasibility Gates")
para("Every incumbent replicate and every redesign candidate was evaluated with the same radial branch-flow "
     f"calculation at {VLL} V line-to-line, power factor {PF}, and aluminium resistivity {RHO:.3e} Ω·m. Demand was "
     f"diversified with a coincidence factor of {CF}. An alternative was feasible only if it was radial and connected, "
     "no branch current exceeded the ampacity of its conductor ("
     + ", ".join(f"{AMP[k]} A for {k} mm²" for k in sorted(AMP)) +
     f"), the coincident cluster load did not exceed the {KVA:.0f} kVA transformer rating, and the cumulative voltage "
     f"drop from the source to any node did not exceed {VD:.0f}%. A cluster entered the economic comparison only if "
     "its least-cost redesign was feasible and at least one incumbent replicate passed the ampacity gate with the "
     "reference conductor; because the transformer load is common to both alternatives and the incumbent voltage drops "
     f"in feasible clusters were at most {VDMAX:.2f}%, every incumbent replicate in the comparison set satisfied all "
     "gates. If the least-cost redesign violated the voltage gate, the cluster was excluded even when a more expensive "
     "candidate might have been feasible; this rule is conservative with respect to the value of reconfiguration.")
h2("Life-Cycle Cost Model")
para("The net present cost (NPC) of an alternative S was computed as")
eq("npc")
para("where C(S) is the capital cost of trenching, duct bank, and cable plus the transformer unit, E(S) is the "
     "annual energy loss, p_e is the value of energy, ω is the annual operation and maintenance fraction of capital "
     f"cost, i is the discount rate, and H is the horizon. The frozen primary values are H = {H} years, i = {DR:.0f}%, "
     f"p_e = {EK} JPY/kWh, ω = {OMF:.1f}%, excavation {n(EXC)} JPY/m, duct bank {n(DUCT)} JPY/m, reference cable "
     f"{n(CAB)} JPY/m (scaled by conductor area), and transformer {n(XF)} JPY. Annual losses were computed from peak "
     f"branch losses with a load factor of {LF}. All costs are in Japanese yen at constant prices.")
h2("Value of Reconfiguration")
para("For cluster c with incumbent replicates r = 1, …, R_c and redesign candidates k ∈ K_c, the value of "
     "reconfiguration (VoF) is")
eq("vof")
para("Retaining the incumbent is an admissible decision, so VoF_c is zero whenever no feasible redesign is cheaper "
     "than the reconstructed incumbent and positive otherwise. Averaging over replicates carries reconstruction "
     "uncertainty into the estimand. Because the redesign may change both topology and conductor sizes, VoF measures "
     "the value of re-layout with re-sizing; a topology-only variant with the reference conductor was computed as an "
     "ablation. Zone-level VoF is reported as a cost-weighted share of like-for-like NPC,")
eq("vofz")
para("where F_z is the set of feasible clusters in zone z and the bar denotes the replicate mean. Cluster VoF "
     f"values below {POS_TOL:g}% of incumbent NPC were treated as numerical zeros. For comparison, a secondary naive "
     "contrast was computed as the difference between mean incumbent NPC and the NPC of the best redesign without "
     "the max operator, that is, with the incumbent excluded from the choice set; this contrast can be negative and is "
     "reported only to show the effect of excluding the incumbent.")
h2("Equivalence Margin and Sensitivity Analyses")
para(f"Before the results were examined, a practical-equivalence margin of {MARGIN:.0f}% of like-for-like NPC was "
     "fixed: zone-level reconfiguration value below this margin is interpreted as economically equivalent to "
     "like-for-like renewal, values above it as beneficial, and estimates whose uncertainty crosses the margin as "
     "indeterminate. Engineering-assumption sensitivity was assessed by re-running the full pipeline with the "
     "medium-voltage threshold at 120 and 200 kW, the cluster target load at 80 kW, the coincidence factor at 0.5, "
     "0.7, and 0.8, and the 24-replicate ensemble. Boundary variants with 80 and 130 kVA transformer limits were also "
     "examined. Economic sensitivity of the naive contrast was assessed by a one-at-a-time tornado analysis over "
     f"discount rate, energy value, horizon, load factor, operation and maintenance fraction, and cost multiplier, and by "
     f"a {N_MC}-draw Monte Carlo analysis.")
h2("Alternating-Current Validation")
para("The linear branch-flow model (Gan and Low 2014) was compared with full alternating-current (AC) power flow in "
     "pandapower (Thurner et al. 2018) for every feasible cluster with a genuine topology choice. For each such "
     "cluster, the first incumbent replicate and a least-cost redesign were modeled with a slack bus at the source, "
     "coincident loads at the stated power factor, per-edge resistance for the reference conductor, and a reactance "
     "of 0.08 Ω/km. Agreement was assessed by the voltage-magnitude difference, the relative loss error, and agreement "
     f"on the {VD:.0f}% voltage-drop gate. The primary check loads each feeder only at its own cluster terminals, as in "
     "the economic comparison. A stress case that also loads customer nodes of neighboring clusters lying on the "
     "reconstructed incumbent tree is reported separately.")
h2("Conditions Associated with Positive Value")
para("To indicate where detailed engineering might be worthwhile, cluster VoF was related descriptively to "
     "interpretable street-network and demand descriptors in the tradition of planar street-network analysis "
     "(Cardillo et al. 2006; Boeing 2020): number of demand terminals, coincident demand, convex-hull "
     "area, demand density on hull and 100-m buffer supports, road density, mean road-edge length and node degree, "
     "incumbent route length per terminal, and spatial span. Pooled Spearman rank correlations were computed with "
     "and without rank-residual adjustment for terminal count. Spatial dependence of cluster VoF within each zone was "
     "summarized by Moran's I with inverse-distance weights and 200 permutations. Because clusters are nested in "
     "three purposive zones and the distribution of VoF is dominated by zeros, these analyses are descriptive.")

h1("Results")
h2("Reconstructed Infrastructure and Feasibility")
para(f"The three study zones contain {n(N_all)} transformer-zone clusters with {MW_all:.1f} MW of modeled "
     f"low-voltage peak demand (Table 1). Of these, {n(NF)} clusters ({MW_f:.1f} MW) passed the feasibility gates and "
     f"entered the economic comparison: {N_f['sano']} in Sano, {N_f['kudamatsu']} in Kudamatsu, and {N_f['yasu']} in "
     f"Yasu (Table 2). {n(SINGLE)} of the feasible clusters serve a single customer node and therefore offer no "
     f"topology choice; the remaining {n(NNT)} clusters have a genuine choice between the incumbent and at least one "
     "alternative layout. Across feasible clusters, the least-cost redesign seldom changed the corridor length "
     "materially relative to the reconstructed incumbent (Fig. 3).")
h2("Magnitude and Distribution of Reconfiguration Value")
para(f"Zone-level VoF was {vz} of like-for-like NPC in Sano, Kudamatsu, and Yasu, respectively (Table 2). All three "
     f"values lie well inside the {MARGIN:.0f}% practical-equivalence margin (Fig. 4). Restricting the denominator to "
     f"clusters with a topology choice changes these values only slightly ({p2(VOF_NT['sano'])}%, "
     f"{p2(VOF_NT['kudamatsu'])}%, and {p2(VOF_NT['yasu'])}%). VoF was positive in {NPOS} of {n(NF)} feasible "
     f"clusters ({100*NPOS/NF:.1f}%), or {100*NPOS/NNT:.1f}% of the clusters with a topology choice (Table 3; Fig. 5). "
     f"Conditional on being positive, the median cluster VoF was {MEDC['sano']:.2f}%, {MEDC['kudamatsu']:.2f}%, and "
     f"{MEDC['yasu']:.2f}% of cluster NPC, and the maximum was {MAXC['sano']:.2f}%, {MAXC['kudamatsu']:.2f}%, and "
     f"{MAXC['yasu']:.2f}%. Value is therefore rare and concentrated in a few clusters rather than spread thinly "
     "across the network.")
para(f"The secondary naive contrast, which excludes the incumbent from the choice set, was {p2(sr.loc['sano','ltp_pct'])}%, "
     f"{p2(NAIVE_K)}%, and {p2(sr.loc['yasu','ltp_pct'])}% (Table 2). The large negative Kudamatsu value arises because "
     "a few small, spatially extended clusters have no redesign cheaper than the incumbent corridor; forcing a "
     "redesign there adds cost without compensating loss reduction. This value is an artifact of the comparator, not "
     "evidence that reconfiguration is harmful when the incumbent remains available.")
h2("Geographic Variation")
para(f"VoF was lowest in Sano, the zone with the most constrained reconstruction (tier 1), and highest in Kudamatsu "
     f"(tier 2), with Yasu (tier 3) intermediate (Fig. 4). The positive-value incidence followed the same order: "
     f"{N_pos['sano']} of {N_f['sano']} feasible clusters in Sano, {N_pos['kudamatsu']} of {N_f['kudamatsu']} in "
     f"Kudamatsu, and {N_pos['yasu']} of {N_f['yasu']} in Yasu (Table 3). Because observability tier, settlement form, "
     "and demand density vary together across only three zones, these differences cannot be attributed to any single "
     "factor; in particular, weaker observability may admit more reconstructed incumbents that a redesign can improve "
     f"on. Within zones, Moran's I of cluster VoF ranged from {MORAN[0]:.3f} to {MORAN[1]:.3f} (smallest permutation "
     f"p = {MORAN_P:.2f}), giving no indication of spatial clustering, although a non-significant result in "
     "zero-dominated data cannot prove its absence.")
h2("Conditions Associated with Positive Value")
para(f"In pooled rank correlations, cluster VoF increased with the number of demand terminals (ρ = {rho('terminals'):.2f}), "
     f"spatial span ({rho('span_m'):.2f}), convex-hull area ({rho('hull_area_km2'):.2f}), and incumbent route length per "
     f"terminal ({rho('route_len_per_terminal_m'):.2f}) (Table 4). After rank-residual adjustment for terminal count, "
     f"these associations fell to {rho('span_m','rho_adj_terminals'):.2f}, {rho('hull_area_km2','rho_adj_terminals'):.2f}, "
     f"and {rho('route_len_per_terminal_m','rho_adj_terminals'):.2f}, respectively. Demand density was not consistent "
     f"across spatial supports (hull ρ = {rho('demand_density_hull_kw_km2'):.2f}; buffer ρ = "
     f"{rho('demand_density_buffer_kw_km2'):.2f}). Larger clusters mechanically offer more alternative routes, and no "
     "independent urban-form correlate of reconfiguration value was found beyond cluster size. For screening, the "
     "practical signal is simply that positive value, when it occurs, occurs in larger clusters.")
h2("Robustness and Sensitivity")
para(f"Across the {N_VAR} engineering-assumption variants, zone VoF ranged from {VMIN:.3f}% to {VMAX:.3f}% and never "
     f"reached the {MARGIN:.0f}% margin (Table 5). The largest values occurred when the medium-voltage threshold was "
     "raised to 200 kW, which admits larger customers and more branched clusters to the low-voltage network; the "
     "smallest occurred with an 80 kW cluster target, which produces smaller clusters with fewer routing alternatives. "
     f"The maximum voltage drop among feasible clusters in any variant was {VDMAX_ENG:.2f}%. The 24-replicate ensemble "
     "changed zone VoF by less than 0.04 percentage points. The economic sensitivity analyses apply to the naive "
     f"contrast: in Kudamatsu all {N_MC} Monte Carlo draws remained negative (5th–95th percentile "
     f"{MC_K5:.2f} to {MC_K95:.2f} billion JPY), whereas in Sano and Yasu the contrast remained positive but small, so "
     "the sign pattern is not an artifact of a particular price or discount assumption. Decomposition of the "
     "incumbent-minus-redesign difference into capital, discounted loss, and residual terms shows that capital "
     "differences dominate and loss savings are small at low-voltage scale (Fig. 6).")
h2("Engineering Validation")
para(f"Full AC power flow converged for all {n(AC1['n'])} feeder–scenario objects in {n(AC1['cl'])} clusters (Table 6). "
     f"With feeders loaded at their own cluster terminals, the linear screen and AC power flow agreed on feasibility in "
     f"every case ({AC1['both']} of {AC1['n']} feasible under both); the maximum voltage-magnitude difference was "
     f"{AC1['dvmax']:.4f} per unit, the maximum relative loss error was {AC1['lmax']:.3f}, and the maximum voltage drop "
     f"was {AC1['lin']:.2f}% (linear) and {AC1['ac']:.2f}% (AC), leaving at least {VD-AC1['ac']:.2f} percentage points "
     f"of margin to the {VD:.0f}% gate. In the stress case, feasibility agreement remained complete, but two incumbent "
     f"replicates in Sano exceeded the gate under both models (maximum drop {AC0['lin']:.2f}% linear and "
     f"{AC0['ac']:.2f}% AC), and the maximum voltage difference rose to {AC0['dvmax']:.4f} per unit. These cases "
     "illustrate how sensitive voltage feasibility is to the reconstructed load assignment, but they do not enter the "
     "economic comparison.")

h1("Discussion")
h2("Why Feasible Redesign Yields Little Economic Benefit")
para("The central result is that, once engineering feasibility and the incumbent option are respected, renewal-time "
     "reconfiguration of these low-voltage networks offers little economic value. Two features of the problem explain "
     "this. First, life-cycle cost at low voltage is dominated by corridor length through excavation and duct costs, "
     "while loss costs are small; a redesign must therefore shorten the corridor to pay, and on a road-constrained "
     "conduit space the incumbent route is usually already close to the shortest feasible connection. Second, the "
     "feasibility gates remove many apparently attractive alternatives: treating raw building peaks as undiversified "
     "loads or ignoring voltage limits creates fictitious headroom and therefore fictitious savings. Within these "
     "reconstructed, demand-constrained networks, successive locally economical connections can leave an inherited "
     "layout close to its current cost minimum, although the historical evolution of the actual networks was not "
     "observed.")
h2("Incumbent-Admissible Comparison")
para("The difference between the primary estimand and the naive contrast is substantive for infrastructure "
     "decision-making. In Kudamatsu, a forced-redesign comparison reports a cost penalty of about "
     f"{abs(NAIVE_K):.0f}%, which could be misread as evidence against reconfiguration in general, whereas the "
     "incumbent-admissible estimand shows that the zone contains several clusters where redesign is worthwhile and "
     "many where it is simply not exercised. This mirrors the treatment of flexibility as an option in infrastructure "
     "planning (Basupi and Kapelan 2015; Zahed et al. 2020). The contribution of the present study is not the "
     "non-negativity of VoF, which follows from the formulation, but the demonstration that its magnitude can be "
     "estimated from reconstructed networks under explicit feasibility gates and compared with a prespecified "
     "equivalence margin.")
h2("Use as a Screening Step under Incomplete Records")
para("The method is intended as a screening step in renewal programs, not as a design tool. Its inputs are open "
     "data, its outputs identify the clusters where detailed reconfiguration engineering might be worth "
     "commissioning, and its zero-dominated results imply that most clusters can proceed with like-for-like "
     "renewal. This supports the decision-support role of reconstructed networks advocated in work on asset "
     "management with incomplete data (Moghtadernejad et al. 2023; Dehghani et al. 2025) and parallels the evaluation "
     "of data procurement as a life-cycle decision (Leo and Swei 2021): screening is useful if the cost of detailed "
     "engineering in the flagged clusters is smaller than the value it uncovers. The present study did not measure "
     "the cost of operating such a screening program or the savings that a utility would realize; the screening "
     "value is therefore a hypothesis supported by the concentration of VoF, not a measured benefit. Integration with "
     "existing renewal scheduling and coordinated work packaging (Dao et al. 2019; Abu-Samra et al. 2020; Kerwin and "
     "Adey 2021) would allow flagged clusters to be prioritized when corridor works are already planned.")
h2("Evidence Needed before Operational Deployment")
para("Several forms of evidence are needed before the method could support utility investment decisions. The "
     "reconstructed incumbents should be compared with actual utility network records for a sample of clusters, as "
     "has been done for synthetic water distribution models (Fletcher et al. 2026). The cost model should be "
     "calibrated against utility unit costs and construction constraints, including traffic management, other buried "
     "utilities, and customer outages. The flagged clusters should be checked with detailed engineering design to "
     "determine whether the modeled savings survive. Finally, applying the method to a larger and less purposive set "
     "of zones would show whether the low magnitudes found here are typical.")
h2("Limitations")
para("The results are conditional on reconstructed rather than fully observed networks: security-light anchors and "
     "road graphs do not observe actual cable routes, and reconstruction uncertainty is represented only by the "
     "replicate ensemble. The three zones were selected purposively for data availability, differ in observability, "
     "and do not support inference to Japanese or other municipalities. Demand, coincidence, the voltage-drop limit, "
     "the low-voltage/medium-voltage boundary, and unit costs are modeling assumptions; several of them move the naive "
     "contrast materially, although none moved zone VoF above the margin. Economic uncertainty intervals were computed "
     "for the naive contrast rather than for VoF itself. The electrical model is a balanced three-phase radial "
     "approximation without unbalance, harmonics, protection coordination, or future load growth and distributed "
     "generation. The candidate set is enumerated rather than exhaustive. The method has not been validated against "
     "utility investment decisions, and institutional, regulatory, and construction constraints that would restrict "
     "or enable reconfiguration in practice were not modeled. The magnitudes reported here should therefore be read "
     "as modeled, zone-specific screening estimates rather than realized savings.")

h1("Conclusions")
para("Scheduled renewal creates an opportunity to reconfigure buried infrastructure at marginal cost, but a feasible "
     "redesign is not automatically a worthwhile one. This study defined the value of reconfiguration at renewal as "
     "the expected life-cycle cost saving of the best feasible redesign relative to an admissible incumbent, and "
     "estimated it for reconstructed low-voltage distribution networks in three Japanese undergrounding study zones. "
     f"Zone-level value was {vz} of like-for-like life-cycle cost, within a prespecified {MARGIN:.0f}% "
     "equivalence margin and robust to engineering and economic assumptions; positive value occurred in "
     f"{100*NPOS/NF:.1f}% of feasible clusters and was concentrated in larger clusters. For infrastructure managers, "
     "the implication is that like-for-like renewal is a defensible default for such networks and that reconfiguration "
     "assessment should be targeted rather than universal. The broader contribution to infrastructure-systems practice "
     "is a feasibility-gated, incumbent-admissible screening procedure that can be applied with open data where "
     "records are incomplete, together with an explicit statement of the evidence required before its outputs inform "
     "investment.")

DAS = [
 "Some or all data, models, or code generated or used during the study are available in a repository online in "
 "accordance with funder data retention policies.",
 "Some or all data, models, or code used during the study were provided by a third party. Direct requests for these "
 "materials may be made to the provider as indicated in the Acknowledgements.",
 "The analysis code, configuration files, source registry with checksums, and all generated machine-readable "
 "results (cluster-level results, sensitivity analyses, AC validation tables, and morphology and spatial "
 "diagnostics) are available in a public repository (Onishi 2026). Road and building data are from OpenStreetMap "
 "under the Open Database License (OpenStreetMap Contributors 2026); security-light records are municipal open "
 "data from Kudamatsu City under CC BY (Kudamatsu City n.d.) and from Sano City under its open-data terms (Sano City "
 "n.d.); map layers use geoBoundaries (CC BY 4.0; Runfola et al. 2020) and Natural Earth (public domain; Natural "
 "Earth n.d.). Third-party raw inputs are not redistributed where their terms do not permit it; their source URLs, "
 "retrieval dates, and checksums are documented in the repository so that they can be retrieved from the "
 "providers.",
]
ACK = ("This research received no specific funding. The author thanks Sano City and Kudamatsu City for publishing "
       "security-light records as open data, and the OpenStreetMap contributors. The author declares no competing "
       "interests.")
AI = ("During the preparation of this work, the author used an AI-based coding and writing assistant (Devin, "
      "Cognition AI) to scaffold and review analysis code, check numerical consistency between outputs and text, "
      "retrieve and verify bibliographic metadata, and draft and edit portions of the manuscript text. The author "
      "reviewed and edited all content, verified all reported results against the generated outputs, and takes full "
      "responsibility for the content of the publication. No AI tool is listed as an author.")

CAPTIONS = [
 "Fig. 1. Data-to-decision pipeline: open geospatial inputs, reconstruction of incumbent networks, engineering "
 "feasibility gates, and the incumbent-admissible renewal comparison.",
 "Fig. 2. Study zones: (a) municipal locations in Japan (prefecture boundaries from geoBoundaries, CC BY 4.0; "
 "coastlines from Natural Earth, public domain); (b–d) road graph (gray) and snapped building demand nodes in Sano, "
 "Kudamatsu, and Yasu (map data © OpenStreetMap contributors, ODbL).",
 "Fig. 3. Route length of the least-cost feasible redesign versus the reconstructed incumbent for all feasible "
 "clusters (log–log axes).",
 f"Fig. 4. Value of reconfiguration by zone (percentage of like-for-like net present cost) and Monte Carlo mean of "
 f"the secondary naive contrast; the shaded band is the prespecified ±{MARGIN:.0f}% practical-equivalence margin.",
 f"Fig. 5. Cluster-level value of reconfiguration: positive-value incidence by zone and magnitudes for the {NPOS} "
 "clusters with positive value.",
 f"Fig. 6. Decomposition of the zone-level incumbent-minus-redesign cost difference into capital, discounted loss, "
 f"and residual terms (billion JPY, {H}-year horizon), with aggregate value of reconfiguration; panels use "
 "independent vertical scales.",
]
REFS["Hadjidemetriou et al. 2022"] = ('Hadjidemetriou, G. M., J. Teal, L. Kapetas, and A. K. Parlikad. 2022. "Flexible '
    'planning for intercity multimodal transport infrastructure." J. Infrastruct. Syst. 28 (1): 05021010. '
    'https://doi.org/10.1061/(ASCE)IS.1943-555X.0000664.')
D24 = max(abs(eng[(eng.parameter == "n_replicates=24") & (eng.city == z)].vof_pct.iloc[0] - VOF[z]) for z in Z)
S[:] = [(k, t.replace("changed zone VoF by less than 0.04 percentage points",
                      f"changed zone VoF by at most {D24:.3f} percentage points")) for k, t in S]
# cost decomposition check for the Fig. 6 sentence
ADF = sum(1 / (1 + DR / 100) ** y for y in range(1, H + 1))
cap_d = sum((f.s1_capex_mean - f.s2_capex).abs().sum() for f in fe.values())
loss_d = sum(((f.s1_plkw_mean - f.s2_plkw) * 8760 * LF * EK * ADF).abs().sum() for f in fe.values())
print(f"decomposition |capex diff| {cap_d/1e9:.3f} bn vs |loss-NPC diff| {loss_d/1e9:.3f} bn JPY")
assert cap_d > loss_d, "Fig. 6 sentence 'capital differences dominate' not supported"


CUTS = [
 ("Incumbent networks are reconstructed as ensembles from open data in three Japanese study zones that differ in record observability; candidate redesigns are generated on the road network; every alternative, including the incumbent, must pass explicit engineering feasibility gates before any cost comparison; and the value of reconfiguration is defined as the expected life-cycle cost saving of the best feasible redesign relative to an admissible incumbent. ", ""),
 (" For screening, the practical signal is simply that positive value, when it occurs, occurs in larger clusters.", ""),
 ("The largest values occurred when the medium-voltage threshold was raised to 200 kW, which admits larger customers and more branched clusters to the low-voltage network; the smallest occurred with an 80 kW cluster target, which produces smaller clusters with fewer routing alternatives.",
  "The largest values occurred with a 200 kW medium-voltage threshold and the smallest with an 80 kW cluster target."),
 (" Within these reconstructed, demand-constrained networks, successive locally economical connections can leave an inherited layout close to its current cost minimum, although the historical evolution of the actual networks was not observed.", ""),
 ("This supports the decision-support role of reconstructed networks advocated in work on asset management with incomplete data (Moghtadernejad et al. 2023; Dehghani et al. 2025) and parallels the evaluation of data procurement as a life-cycle decision (Leo and Swei 2021): screening is useful if",
  "As with data procurement decisions (Leo and Swei 2021), screening is useful if"),
 ("Several forms of evidence are needed before the method could support utility investment decisions. The reconstructed incumbents should be compared with actual utility network records for a sample of clusters, as has been done for synthetic water distribution models (Fletcher et al. 2026). The cost model should be calibrated against utility unit costs and construction constraints, including traffic management, other buried utilities, and customer outages. The flagged clusters should be checked with detailed engineering design to determine whether the modeled savings survive. Finally, applying the method to a larger and less purposive set of zones would show whether the low magnitudes found here are typical.",
  "Before the method could support utility investment decisions, reconstructed incumbents should be compared with utility network records for a sample of clusters, as has been done for synthetic water distribution models (Fletcher et al. 2026); unit costs and construction constraints such as traffic management, other buried utilities, and customer outages should be calibrated with utilities; flagged clusters should be checked by detailed design; and a larger, less purposive set of zones should be analyzed to test whether the low magnitudes found here are typical."),
 (" The broader contribution to infrastructure-systems practice is a feasibility-gated, incumbent-admissible screening procedure that can be applied with open data where records are incomplete, together with an explicit statement of the evidence required before its outputs inform investment.",
  " The broader contribution is a feasibility-gated, incumbent-admissible screening procedure that can be applied with open data where records are incomplete."),
 ("Two features of the problem explain this. ", ""),
 (" Because the incumbent is always admissible, this value cannot be negative; its non-negativity is a property of the decision formulation, not an empirical finding.",
  " Because the incumbent is always admissible, this value cannot be negative by construction; non-negativity is not an empirical finding."),
]
for a, b in CUTS:
    hit = [i for i, (k, t) in enumerate(S) if a in t]
    assert len(hit) == 1, a[:60]
    k, t = S[hit[0]]; S[hit[0]] = (k, t.replace(a, b))


CUTS2 = [
 (" Value is therefore rare and concentrated in a few clusters rather than spread thinly across the network.", ""),
 (", which could be misread as evidence against reconfiguration in general, whereas", ", whereas"),
 ("Undergrounding programs are justified mainly by resilience, safety, and streetscape objectives, and economic studies show",
  "Economic studies show"),
 (", unlike approaches that treat surface features as network nodes (Chahinian et al. 2019). The evidence available in each tier determined how strongly the reconstruction was constrained, following the logic of integration under incomplete semantics (Gilbert et al. 2021).",
  "; the evidence available in each tier determined how strongly the reconstruction was constrained."),
 ("(Haklay and Weber 2008; OpenStreetMap Contributors 2026)", "(OpenStreetMap Contributors 2026)"),
 ("Samui et al. 2012; Kumar et al. 2014)", "Samui et al. 2012)"),
 ("(Hadzilacos et al. 2000; Hastak and Gokhale 2000; Khan et al. 2015)", "(Hastak and Gokhale 2000; Khan et al. 2015)"),
 ("interpretable street-network and demand descriptors in the tradition of planar street-network analysis (Cardillo et al. 2006; Boeing 2020): number of demand terminals, coincident demand, convex-hull area, demand density on hull and 100-m buffer supports, road density, mean road-edge length and node degree, incumbent route length per terminal, and spatial span.",
  "ten street-network and demand descriptors (Cardillo et al. 2006; Boeing 2020), including terminal count, coincident demand, convex-hull area, demand density on hull and 100-m buffer supports, road density, and incumbent route length per terminal."),
 ("materially relative to the reconstructed incumbent (Fig. 3).",
  "materially relative to the reconstructed incumbent (Fig. S1 in the Supplemental Materials)."),
]
for a, b in CUTS2:
    hit = [i for i, (k, t) in enumerate(S) if a in t]
    assert len(hit) == 1, a[:60]
    k, t = S[hit[0]]; S[hit[0]] = (k, t.replace(a, b))
for old, new in (("Fig. 4", "Fig. 3"), ("Fig. 5", "Fig. 4"), ("Fig. 6", "Fig. 5")):
    S[:] = [(k, t.replace(old, new)) for k, t in S]
SUPP_CAPTION = CAPTIONS.pop(2).replace("Fig. 3.", "Fig. S1.")
CAPTIONS[:] = [c.replace("Fig. 4.", "Fig. 3.").replace("Fig. 5.", "Fig. 4.").replace("Fig. 6.", "Fig. 5.") for c in CAPTIONS]
CAPTIONS[1] = ("Fig. 2. Study zones: (a) locations in Japan (boundaries: geoBoundaries, CC BY 4.0; coastlines: Natural "
               "Earth); (b–d) road graph and snapped demand nodes in Sano, Kudamatsu, and Yasu (map data © "
               "OpenStreetMap contributors, ODbL).")
for k in ("Haklay and Weber 2008", "Chahinian et al. 2019", "Gilbert et al. 2021", "Kumar et al. 2014", "Hadzilacos et al. 2000"):
    REFS.pop(k)
CAPTIONS[0] = "Fig. 1. Data-to-decision pipeline from open geospatial inputs to the incumbent-admissible renewal comparison."
CAPTIONS[2] = (f"Fig. 3. Value of reconfiguration by zone (% of like-for-like NPC) and Monte Carlo mean of the naive "
               f"contrast; shaded band: ±{MARGIN:.0f}% equivalence margin.")
CAPTIONS[4] = (f"Fig. 5. Zone-level incumbent-minus-redesign cost difference by component (billion JPY, {H}-year "
               "horizon) and aggregate value of reconfiguration; panels use independent vertical scales.")
N_FIG = len(CAPTIONS)


for old, new in (("VoF_c", "VoF<sub>c</sub>"), ("R_c", "R<sub>c</sub>"), ("K_c", "K<sub>c</sub>"),
                 ("p_e", "p<sub>e</sub>"), ("F_z", "F<sub>z</sub>")):
    S[:] = [(k, t.replace(old, new) if k == "p" else t) for k, t in S]
S[:] = [(k, t.replace(f"{RHO:.3e} Ω·m", "2.826 × 10<sup>−8</sup> Ω·m").replace(f"{POS_TOL:g}%", "10<sup>−6</sup>%"))
        for k, t in S]
assert not any("e-0" in t for k, t in S), "unformatted exponent left in text"

# ---------------------------------------------------------------- word checks
def wc(t): return len(re.findall(r"\S+", t))
assert 250 <= wc(ABSTRACT) <= 300, wc(ABSTRACT)
assert 150 <= wc(PRACTICAL) <= 200, wc(PRACTICAL)
assert not re.search(r"\(\D+ \d{4}\)", ABSTRACT)

# ---------------------------------------------------------------- docx helpers
MNS = ('xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
       'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"')
RPR = '<w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/><w:color w:val="000000"/><w:sz w:val="24"/></w:rPr>'
def mr(t, plain=False):
    sty = '<m:rPr><m:sty m:val="p"/></m:rPr>' if plain else ''
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f'<m:r>{sty}{RPR}<m:t xml:space="preserve">{t}</m:t></m:r>'
def e(x): return f"<m:e>{x}</m:e>"
def ssub(b, s): return f"<m:sSub><m:e>{b}</m:e><m:sub>{s}</m:sub></m:sSub>"
def ssup(b, s): return f"<m:sSup><m:e>{b}</m:e><m:sup>{s}</m:sup></m:sSup>"
def frac(a, b): return f"<m:f><m:num>{a}</m:num><m:den>{b}</m:den></m:f>"
def nsum(lo, hi, body):
    sup = f"<m:sup>{hi}</m:sup>" if hi else "<m:sup/>"
    hide = "" if hi else '<m:supHide m:val="1"/>'
    return (f'<m:nary><m:naryPr><m:chr m:val="∑"/><m:limLoc m:val="undOvr"/>{hide}</m:naryPr>'
            f"<m:sub>{lo}</m:sub>{sup}<m:e>{body}</m:e></m:nary>")
def delim(x, b="(", c=")"):
    return mr(b, True) + x + mr(c, True)
def func(name, arg, lim=None):
    nm = mr(name, True)
    if lim:
        nm = f"<m:limLow><m:e>{nm}</m:e><m:lim>{lim}</m:lim></m:limLow>"
    return f"<m:func><m:fName>{nm}</m:fName><m:e>{arg}</m:e></m:func>"
def bar(x): return f'<m:bar><m:barPr><m:pos m:val="top"/></m:barPr><m:e>{x}</m:e></m:bar>'
NPC = mr("NPC", True)
EQ = {
 "npc": NPC + delim(mr("S")) + mr("=") + mr("C") + delim(mr("S")) + mr("+") +
        nsum(mr("t=1"), mr("H"), frac(ssub(mr("p"), mr("e")) + mr("E") + delim(mr("S")) + mr("+ω") + mr("C") + delim(mr("S")),
                                        ssup(delim(mr("1+i")), mr("t")))),
 "vof": ssub(mr("VoF", True), mr("c")) + mr("=") + frac(mr("1"), ssub(mr("R"), mr("c"))) +
        nsum(mr("r=1"), ssub(mr("R"), mr("c")),
             func("max", delim(mr("0, ") + NPC + delim(ssub(mr("S1"), mr("c,r"))) + mr("−") +
                  func("min", NPC + delim(ssub(mr("S2"), mr("c,k"))), mr("k∈") + ssub(mr("K"), mr("c"))), "{", "}"))),
 "vofz": ssub(mr("VoF%", True), mr("z")) + mr("=100") +
         frac(nsum(mr("c∈") + ssub(mr("F"), mr("z")), None, ssub(mr("VoF", True), mr("c"))),
              nsum(mr("c∈") + ssub(mr("F"), mr("z")), None, bar(NPC) + delim(ssub(mr("S1"), mr("c"))))),
}
EQN = {"npc": 1, "vof": 2, "vofz": 3}

doc = docx.Document()
sec = doc.sections[0]
from docx.shared import Inches
sec.page_width, sec.page_height = Inches(8.5), Inches(11)
for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
    setattr(sec, side, Inches(1))
ln = OxmlElement("w:lnNumType"); ln.set(qn("w:countBy"), "1"); ln.set(qn("w:restart"), "continuous")
sec._sectPr.append(ln)

def fix_style(st, size=12, bold=None, italic=None):
    st.font.name = "Times New Roman"; st.font.size = Pt(size); st.font.color.rgb = RGBColor(0, 0, 0)
    if bold is not None: st.font.bold = bold
    if italic is not None: st.font.italic = italic
    rpr = st.element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts"); rpr.insert(0, rf)
    for a in list(rf.attrib):
        del rf.attrib[a]
    for a in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rf.set(qn(a), "Times New Roman")
    pf = st.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.DOUBLE; pf.space_before = Pt(0); pf.space_after = Pt(0)
fix_style(doc.styles["Normal"])
fix_style(doc.styles["Heading 1"], bold=True, italic=False)
fix_style(doc.styles["Heading 2"], bold=True, italic=True)
for hs in ("Heading 1", "Heading 2"):
    doc.styles[hs].paragraph_format.space_before = Pt(12); doc.styles[hs].paragraph_format.keep_with_next = True

# footer page number
fp = sec.footer.paragraphs[0]; fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
for tag, txt in (("begin", None), (None, "PAGE"), ("end", None)):
    r = fp.add_run()
    if tag:
        fc = OxmlElement("w:fldChar"); fc.set(qn("w:fldCharType"), tag); r._r.append(fc)
    else:
        it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = txt; r._r.append(it)

def P(text="", bold=False, italic=False, align=None, indent=True, size=None):
    p = doc.add_paragraph()
    if align: p.alignment = align
    if indent and text: p.paragraph_format.first_line_indent = Inches(0.5)
    if text:
        for part in re.split(r"(<su[bp]>.*?</su[bp]>)", text):
            if not part: continue
            m = re.match(r"<(su[bp])>(.*?)</su[bp]>", part)
            r = p.add_run(m.group(2) if m else part); r.bold = bold; r.italic = italic
            if m: r.font.subscript = m.group(1) == "sub"; r.font.superscript = m.group(1) == "sup"
            if size: r.font.size = Pt(size)
    return p
def page_break():
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

# ---------------------------------------------------------------- title page + abstract
P(TITLE, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, indent=False)
P(AUTHOR, align=WD_ALIGN_PARAGRAPH.CENTER, indent=False)
P(AFFIL, align=WD_ALIGN_PARAGRAPH.CENTER, indent=False)
doc.add_heading("Abstract", level=1); P(ABSTRACT, indent=False)
doc.add_heading("Practical Applications", level=1); P(PRACTICAL, indent=False)
P("Author keywords: Infrastructure renewal; Asset management; Undergrounding; Distribution network "
  "reconfiguration; Life-cycle cost; Network reconstruction; Engineering feasibility.", indent=False)

for kind, t in S:
    if kind == "h1": doc.add_heading(t, level=1)
    elif kind == "h2": doc.add_heading(t, level=2)
    elif kind == "p": P(t)
    elif kind == "eq":
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p._p.append(parse_xml(f"<m:oMath {MNS}>{EQ[t]}</m:oMath>"))
        p.add_run(f"\t({EQN[t]})")

doc.add_heading("Data Availability Statement", level=1)
for t in DAS: P(t)
doc.add_heading("Acknowledgments", level=1); P(ACK)
doc.add_heading("Disclosure of AI Tool Use", level=1); P(AI)
doc.add_heading("Supplemental Materials", level=1)
P("Fig. S1 is available online in the ASCE Library (www.ascelibrary.org).")

# ---------------------------------------------------------------- references + cross-check
body = " ".join(t for k, t in S if k == "p") + " " + " ".join(DAS)
cited = set()
for grp in re.findall(r"\(([^()]*?(?:\d{4}|n\.d\.)[a-z]?)\)", body):
    for c in grp.split(";"):
        c = c.strip()
        if re.search(r"(\d{4}|n\.d\.)$", c) and not re.match(r"^\d", c):
            cited.add(c)
for k in REFS:
    if k in body: cited.add(k)
unknown = sorted(c for c in cited if c not in REFS)
uncited = sorted(k for k in REFS if k not in body)
assert not unknown, f"citations without reference: {unknown}"
assert not uncited, f"references never cited: {uncited}"
doc.add_heading("References", level=1)
def surname_key(k): return re.sub(r"[^a-z ]", "", REFS[k].lower().replace("é", "e"))
for k in sorted(REFS, key=surname_key):
    p = P(REFS[k], indent=False)
    p.paragraph_format.left_indent = Inches(0.5); p.paragraph_format.first_line_indent = Inches(-0.5)

# ---------------------------------------------------------------- figure captions
doc.add_heading("Figure Captions", level=1)
for c in CAPTIONS: P(c, indent=False)
assert "Fig. S1" in body
for i in range(1, N_FIG + 1):
    assert f"Fig. {i}" in body, f"Fig. {i} not cited"

# ---------------------------------------------------------------- tables
FIRST_TABLE = [True]
def table(title, header, rows, note=None):
    if FIRST_TABLE[0]:
        page_break(); FIRST_TABLE[0] = False
    else:
        P("").paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    tp = P(title, indent=False); tp.paragraph_format.keep_with_next = True
    tp.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    t = doc.add_table(rows=1, cols=len(header)); t.style = "Table Grid"
    for c, h in zip(t.rows[0].cells, header): c.text = h
    for r in rows:
        cells = t.add_row().cells
        for c, v in zip(cells, r): c.text = re.sub(r'^-(?=\d)', '−', str(v))
    for row in t.rows:
        for c in row.cells:
            for p in c.paragraphs:
                p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
                for r in p.runs: r.font.size = Pt(10)
    for c in t.rows[0].cells:
        for r in c.paragraphs[0].runs: r.bold = True
    if note: P(note, indent=False, size=10).paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE

jme = docx.Document(f"{ROOT}/manuscript/manuscript_jme.docx")
mv = {r.cells[0].text.lower(): r.cells[3].text for r in jme.tables[0].rows[1:]}
tier = {"sano": "1: pole-linked anchors", "kudamatsu": "2: geolocated anchors", "yasu": "3: roads and buildings only"}
table("Table 1. Study zones, observability tiers, and cluster counts",
      ["Zone", "Observability tier", "LV demand, all clusters (MW)", "MV-excluded demand (MW)", "Clusters",
       "Feasible clusters", "Feasible single-customer clusters"],
      [[ZN[z], tier[z], f"{sr.loc[z,'lv_demand_kw']/1e3:.1f}", mv[z], len(rc[z]), N_f[z], N_f[z]-N_nt[z]] for z in Z]
      + [["Total", "", f"{MW_all:.1f}", "", N_all, NF, SINGLE]],
      "Note: LV = low voltage; MV = medium voltage. MV-excluded demand is from buildings above the LV/MV threshold.")
table("Table 2. Zone-level life-cycle cost and value of reconfiguration (feasible clusters)",
      ["Zone", "Feasible clusters", "Feasible demand (MW)", "NPC like-for-like (billion JPY)",
       "NPC best redesign (billion JPY)", "VoF (million JPY)", "VoF (% of like-for-like NPC)",
       "VoF, clusters with topology choice (%)", "Naive contrast (%)"],
      [[ZN[z], N_f[z], f"{fe[z].raw_kw.sum()/1e3:.1f}", f"{sr.loc[z,'s1_npc']/1e9:.2f}", f"{sr.loc[z,'s2_npc']/1e9:.2f}",
        f"{sr.loc[z,'vof']/1e6:.1f}", f"{VOF[z]:.3f}", f"{VOF_NT[z]:.3f}", f"{sr.loc[z,'ltp_pct']:.2f}"] for z in Z],
      "Note: NPC = net present cost, 40-year horizon, 3% discount rate. The naive contrast excludes the incumbent "
      "from the choice set and is reported for comparison only.")
table("Table 3. Distribution of cluster-level value of reconfiguration",
      ["Zone", "Feasible clusters", "Single-customer (no choice)", "With topology choice", "Positive VoF",
       "Zero share, all feasible", "Zero share, with choice", "Median VoF if positive (%)", "Maximum VoF (%)"],
      [[ZN[z], N_f[z], N_f[z]-N_nt[z], N_nt[z], N_pos[z], f"{1-N_pos[z]/N_f[z]:.3f}", f"{1-N_pos[z]/N_nt[z]:.3f}",
        f"{MEDC[z]:.3f}", f"{MAXC[z]:.3f}"] for z in Z]
      + [["Total", NF, SINGLE, NNT, NPOS, f"{1-NPOS/NF:.3f}", f"{1-NPOS/NNT:.3f}", "", ""]],
      f"Note: Cluster VoF below {POS_TOL:.6f}% of incumbent NPC is treated as zero.")
LAB = {"terminals": "Demand terminals (count)", "coinc_kw": "Coincident demand (kW)",
       "hull_area_km2": "Convex-hull area (km²)", "demand_density_hull_kw_km2": "Demand density, hull (kW/km²)",
       "demand_density_buffer_kw_km2": "Demand density, 100-m buffer (kW/km²)",
       "road_density_km_per_km2": "Road density (km/km²)", "mean_edge_len_m": "Mean road-edge length (m)",
       "mean_degree": "Mean road-node degree", "route_len_per_terminal_m": "Incumbent route length per terminal (m)",
       "span_m": "Spatial span (m)", "tld": "Topology divergence (endogenous diagnostic)"}
table("Table 4. Rank correlation of cluster value of reconfiguration with network and demand descriptors",
      ["Descriptor", "Pooled Spearman ρ", "ρ adjusted for terminal count", "n"],
      [[LAB[p], f"{mor.loc[p,'spearman_rho_pooled']:.2f}",
        "—" if pd.isna(mor.loc[p, "rho_adj_terminals"]) else f"{mor.loc[p,'rho_adj_terminals']:.2f}",
        int(mor.loc[p, "n_used"])] for p in mor.index],
      "Note: Descriptive only; clusters are spatially dependent and nested in three zones. n below the feasible total "
      "reflects degenerate hulls or clusters without internal road edges. Topology divergence is derived from the "
      "reconstruction itself and is not an urban-form predictor.")
VL = {"baseline": "Baseline", "lv_max_node_kw=120": "MV threshold 120 kW", "lv_max_node_kw=200": "MV threshold 200 kW",
      "cluster_target_kw=80": "Cluster target 80 kW", "coincidence=0.5": "Coincidence factor 0.5",
      "coincidence=0.7": "Coincidence factor 0.7", "coincidence=0.8": "Coincidence factor 0.8",
      "n_replicates=24": "24-replicate ensemble"}
rows5 = []
for prm in eng.parameter.drop_duplicates():
    row = [VL.get(prm, prm)]
    for z in Z:
        x = eng[(eng.parameter == prm) & (eng.city == z)].iloc[0]
        row += [int(x.feasible), f"{x.vof_pct:.3f}"]
    rows5.append(row)
table("Table 5. Sensitivity of zone-level value of reconfiguration to engineering assumptions",
      ["Variant", "Sano feasible", "Sano VoF (%)", "Kudamatsu feasible", "Kudamatsu VoF (%)", "Yasu feasible",
       "Yasu VoF (%)"], rows5,
      f"Note: Each variant re-runs reconstruction, gating, and optimization. Prespecified equivalence margin: {MARGIN:.0f}%.")
table("Table 6. Linear feasibility screen versus full AC power flow",
      ["Statistic", "Cluster-terminal loading (primary)", "All-node loading (stress case)"],
      [["Feeder–scenario objects (clusters)", f"{AC1['n']} ({AC1['cl']})", f"{AC0['n']} ({AC0['cl']})"],
       ["Non-converged", AC1["nc"], AC0["nc"]],
       ["Feasibility agreement", f"{AC1['agree']:.3f}", f"{AC0['agree']:.3f}"],
       ["Feasible under both models", AC1["both"], AC0["both"]],
       ["Median |ΔV| (per unit)", f"{AC1['dvmed']:.4f}", f"{AC0['dvmed']:.4f}"],
       ["Maximum |ΔV| (per unit)", f"{AC1['dvmax']:.4f}", f"{AC0['dvmax']:.4f}"],
       ["Maximum relative loss error", f"{AC1['lmax']:.3f}", f"{AC0['lmax']:.3f}"],
       ["Maximum voltage drop, linear (%)", f"{AC1['lin']:.2f}", f"{AC0['lin']:.2f}"],
       ["Maximum voltage drop, AC (%)", f"{AC1['ac']:.2f}", f"{AC0['ac']:.2f}"]],
      "Note: Cluster-terminal loading matches the economic comparison; the stress case also loads customer nodes of "
      "neighboring clusters on the reconstructed incumbent tree. Voltage-drop gate: "
      f"{VD:.0f}%.")
for i in range(1, 7):
    assert f"Table {i}" in body, f"Table {i} not cited"

doc.core_properties.title = TITLE; doc.core_properties.author = AUTHOR
doc.save(OUT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jis_docx_utils import sanitize_docx
sanitize_docx(OUT)
words = sum(wc(t) for k, t in S if k == "p")
print(f"saved {OUT}; body words {words}; abstract {wc(ABSTRACT)}; PA {wc(PRACTICAL)}; refs {len(REFS)}")
