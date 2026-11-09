# JIS Reference Audit

Date: 2026-11-09. Source: reference list of `JIS_MANUSCRIPT_FINAL.docx`, checked by `scripts/p34_reference_audit.py` against Crossref single-work records (raw JSON persisted in `data/raw/journal_jis/crossref_works/`; machine output `analysis/JIS_REFERENCE_CHECK.csv`). Checks: first-author surname, title, year (any of print/online/issued), volume, issue, page/article number. In-text ↔ list consistency is enforced by assertions in `scripts/p32_manuscript_jis.py` (every in-text author–date citation resolves to a list entry and every list entry is cited).

Summary: 36 references; 30 DOI records match Crossref on all fields; 1 flagged and resolved (below); 5 web/data sources without DOI (accessed dates given, as ASCE requires for data citations). 15 references are JIS papers.

Target of 35–45 references: 36 entries, of which 6 are mandatory data/code/map citations required by the ASCE Data Availability policy. Sixteen references from the prior (JME) version were removed as not needed for JIS (three municipal profile pages, Hwang and Richards 1992, Fu et al. 2016, Barthélemy 2011, Haklay and Weber 2008, Chahinian et al. 2019, Gilbert et al. 2021, Kumar et al. 2014, Hadzilacos et al. 2000, Ochs et al. 2014, Camargo et al. 2013, Baran and Wu 1989b, Louf and Barthélemy 2014, Levinson 2012); no reference was added only to raise the count.

Format: ASCE author–date; list alphabetized by first-author surname; ISO-abbreviated journal titles; DOIs as https://doi.org/ links; web sources with "Accessed" dates; Japanese-language sources marked "[in Japanese]".

| # | Reference (first 60 chars) | DOI | Crossref year / vol (issue): page | JIS? | Status | Relevance / where cited |
|---|---|---|---|---|---|---|
| 1 | Abdel-Mottaleb, N., and Q. Zhang. 2020. "Water distribution– | 10.1061/(ASCE)IS.1943-555X.0000563 | 2020 / 26 (3): 04020025 | yes | OK | utility–road colocation; morphology (Intro, Discussion) |
| 2 | Abu-Samra, S., M. Ahmed, and L. Amador. 2020. "Asset managem | 10.1061/(ASCE)IS.1943-555X.0000580 | 2020 / 26 (4): 04020039 | yes | OK | integrated municipal renewal coordination (Intro, Discussion) |
| 3 | Babli, M., T. Gebhard, and E. Brucherseifer. 2025. "Open dat | 10.3390/electronics14071414 | 2025 / 14 (7): 1414 | no | OK | open-data LV grid reconstruction precedent (Intro) |
| 4 | Bandam, A., C. Syranidou, J. Linssen, and D. Stolten. 2021.  | 10.1109/ISGTEurope52324.2021.9639916 | 2021 /  (): 1-6 | no | RESOLVED: Crossref lists given/family names swapped (family 'Abhilash'); IEEE Xplore byline 'Abhilash Bandam' → surname Bandam retained; pages 1–6 per Crossref | geo-referenced synthetic LV networks (Intro) |
| 5 | Baran, M. E., and F. F. Wu. 1989. "Network reconfiguration i | 10.1109/61.25627 | 1989 / 4 (2): 1401-1407 | no | OK | distribution reconfiguration optimization (Intro) |
| 6 | Basupi, I., and Z. Kapelan. 2015. "Evaluating flexibility in | 10.1061/(ASCE)IS.1943-555X.0000199 | 2015 / 21 (2): 04014034 | yes | OK | valuing design flexibility in utility networks (Intro, Discussion) |
| 7 | Boeing, G. 2020. "A multi-scale analysis of 27,000 urban str | 10.1177/2399808318784595 | 2018/2020 / 47 (4): 590-608 | no | OK | street-network descriptors (Methods) |
| 8 | Bynum, M., A. Staid, B. Arguello, A. Castillo, B. Knueven, C | 10.1061/(ASCE)IS.1943-555X.0000603 | 2021 / 27 (2): 04021004 | yes | OK | constrained power-network investment optimization in JIS (Intro) |
| 9 | Cardillo, A., S. Scellato, V. Latora, and S. Porta. 2006. "S | 10.1103/PhysRevE.73.066107 | 2006 / 73 (6): 066107 | no | OK | planar street-network metrics (Methods) |
| 10 | Dao, C. D., A. Hartmann, A. Lamper, and P. Herbert. 2019. "S | 10.1061/(ASCE)IS.1943-555X.0000515 | 2019 / 25 (4): 04019027 | yes | OK | network renewal scheduling (Intro, Discussion) |
| 11 | Dehghani, M. S., Y. Y. Kesete, and S. McNeil. 2025. "Assembl | 10.1061/JITSE4.ISENG-2459 | 2025 / 31 (2): 05025001 | yes | OK | asset management under data scarcity (Intro) |
| 12 | Fenrick, S. A., and L. Getachew. 2012. "Cost and reliability | 10.1016/j.jup.2011.10.002 | 2012 / 20 (1): 31-37 | no | OK | undergrounding cost–reliability economics (Intro) |
| 13 | Fletcher, S., M. Chester, K. Klise, R. Jain, I. Searles, R.  | 10.1061/JITSE4.ISENG-3052 | 2026 / 32 (4): 05026007 | yes | OK | synthetic utility networks vs ground truth (Intro, Discussion) |
| 14 | Gan, L., and S. H. Low. 2014. "Convex relaxations and linear | 10.1109/PSCC.2014.7038399 | 2014 /  (): 1-9 | no | OK | linear branch-flow model (Methods) |
| 15 | Hadjidemetriou, G. M., J. Teal, L. Kapetas, and A. K. Parlik | 10.1061/(ASCE)IS.1943-555X.0000664 | 2022 / 28 (1): 05021010 | yes | OK | flexible infrastructure planning (Intro) |
| 16 | Hastak, M., and S. Gokhale. 2000. "System for evaluating und | 10.1061/(ASCE)1076-0342(2000)6:3(105) | 2000 / 6 (3): 105-113 | yes | OK | underground renewal option evaluation (Intro) |
| 17 | Kerwin, S., and B. T. Adey. 2021. "Integrated planning of op | 10.1061/(ASCE)IS.1943-555X.0000646 | 2021 / 27 (4): 04021039 | yes | OK | integrated distribution-network planning (Intro, Discussion) |
| 18 | Khan, Z., O. Moselhi, and T. Zayed. 2015. "Identifying rehab | 10.1061/(ASCE)IS.1943-555X.0000220 | 2015 / 21 (2): 04014037 | yes | OK | rehabilitation option selection (Intro) |
| 19 | Kou, L., G. Markowsky, and L. Berman. 1981. "A fast algorith | 10.1007/BF00288961 | 1981 / 15 (2): 141-145 | no | OK | Steiner-tree heuristic used (Methods) |
| 20 | Kudamatsu City. n.d. "Security-light inventory [in Japanese] | — | — | no | NO-DOI (web/data source) | data citation: security-light records (Methods, DAS) |
| 21 | Larsen, P. H. 2016. "A method to estimate the costs and bene | 10.1016/j.eneco.2016.09.011 | 2016 / 60 (): 47-61 | no | OK | undergrounding cost–benefit (Intro) |
| 22 | Leo, B., and O. Swei. 2021. "Life-cycle cost analysis framew | 10.1061/(ASCE)IS.1943-555X.0000596 | 2021 / 27 (1): 05020011 | yes | OK | LCCA of data procurement (Intro, Discussion) |
| 23 | Liu, D., J. S. Giraldo, P. Palensky, and P. P. Vergara. 2025 | 10.1016/j.ijepes.2024.110395 | 2025 / 164 (): 110395 | no | OK | LV topology from open GIS (Intro) |
| 24 | Moghtadernejad, S., Y. Jin, and B. T. Adey. 2023. "Estimatin | 10.1061/(ASCE)IS.1943-555X.0000726 | 2023 / 29 (1): 04022041 | yes | OK | missing infrastructure data (Intro) |
| 25 | Natural Earth. n.d. "1:10m physical vectors: Land." Accessed | — | — | no | NO-DOI (web/data source) | map-data citation (DAS, Fig. 2) |
| 26 | Onishi, T. 2026. "underground-topology: Code, configuration, | — | — | no | NO-DOI (web/data source) | code/results repository citation (DAS) |
| 27 | OpenStreetMap Contributors. 2026. "OpenStreetMap road and bu | — | — | no | NO-DOI (web/data source) | data citation: roads/buildings (Methods, DAS) |
| 28 | Runfola, D., et al. 2020. "geoBoundaries: A global database  | 10.1371/journal.pone.0231866 | 2020 / 15 (4): e0231866 | no | OK | geoBoundaries map-data citation (DAS) |
| 29 | Salman, A. M., and Y. Li. 2017. "Assessing climate change im | 10.1061/(ASCE)IS.1943-555X.0000316 | 2017 / 23 (1): 04016024 | yes | OK | power distribution as JIS infrastructure investment (Intro) |
| 30 | Samui, A., S. Singh, T. Ghose, and S. R. Samantaray. 2012. " | 10.1109/TPWRD.2011.2167522 | 2012 / 27 (1): 253-260 | no | OK | feeder routing optimization (Intro) |
| 31 | Sano City. n.d. "Security-light data [in Japanese]." Accesse | — | — | no | NO-DOI (web/data source) | data citation: security-light records (Methods, DAS) |
| 32 | Taheri, B., D. K. Molzahn, and S. Grijalva. 2023. "Improving | 10.1016/j.epsr.2022.108804 | 2023 / 214 (): 108804 | no | OK | targeted undergrounding resilience (Intro) |
| 33 | Thurner, L., A. Scheidler, F. Schafer, J.-H. Menke, J. Dolli | 10.1109/TPWRS.2018.2829021 | 2018 / 33 (6): 6510-6521 | no | OK | pandapower AC validation tool (Methods) |
| 34 | Tram, H. N., and D. L. Wall. 1988. "Optimal conductor select | 10.1109/59.43199 | 1988 / 3 (1): 200-206 | no | OK | conductor selection (Intro) |
| 35 | Zahed, S. E., S. M. Shahandashti, and J. D. Diltz. 2020. "In | 10.1061/(ASCE)IS.1943-555X.0000568 | 2020 / 26 (3): 04020029 | yes | OK | real-options valuation, underground infrastructure (Intro, Discussion) |
| 36 | Zhang, F., Z. Xu, R. Zhu, C. Liang, and D. Gu. 2025. "Geospa | 10.1111/mice.70085 | 2025 / 40 (27): 4884-4903 | no | OK | utility network mapping from imagery/rules (Intro) |

Notes:
- Boeing 2020: Crossref shows online 2018, issue 2020 (47 (4): 590–608); the volume year 2020 is used in text and list.
- Fletcher et al. 2026 (JIS 32 (4)) is a 2026 issue; verified in Crossref.
- Web/data sources (Kudamatsu City n.d., Sano City n.d., OpenStreetMap Contributors 2026, Natural Earth n.d., Onishi 2026) were checked for URL validity at retrieval (source registry `provenance/source_registry.csv`, SHA-256 recorded); live URL availability should be rechecked on the submission date.
- `Onishi 2026` points to the journal-neutral public repository https://github.com/bougtoir/underground-topology; a DOI (e.g., Zenodo) is recommended before acceptance but not required for submission.
