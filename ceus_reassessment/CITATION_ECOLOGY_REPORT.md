# CEUS citation ecology report

## Where the manuscript's evidence actually lives

The study sits at the intersection of three communities that cite little into each other:

1. **Geospatial urban-systems / GIScience** (CEUS's core): urban street-network morphology (Barthélemy 2011; Cardillo et al. 2006; Louf & Barthélemy 2014; Boeing 2020; Levinson 2012), reproducible OSM analytics, geospatial decision support. These papers build descriptors of urban spatial structure but do not connect them to infrastructure investment decisions.
2. **Infrastructure network modelling / reconstruction** (CAIE + ISPRS + power venues): Fu/Wilkinson/Dawson 2016 spatial network evolution model; Zhang et al. 2025 street-view utility mapping; Abhilash Bandam et al. 2021 geo-referenced LV synthesis; Liu et al. TNO OSM+smart-meter topology identification; Synthetic Grid Generator; MDPI land-use reconstruction. These solve *observation*: how to get a plausible network where none is recorded. None value a decision over that reconstruction, and none gate reconstructed topologies by engineering feasibility before comparing them.
3. **Power distribution planning & undergrounding economics** (TPWRD/IJEPES/EPSR/Eneco/UP): Samui 2012, Kumar 2014, Camargo 2013, Baran & Wu, Tram & Wall routing/planning methods; Larsen 2016, Fenrick & Getachew 2012, Taheri 2023 undergrounding economics. Planning methods optimize topology on a fixed/greenfield demand surface; economics papers compare underground vs overhead at system level. Neither poses the renewal-window choice problem: incumbent remains a decision, re-layout has optional value conditional on the incumbent's actual geometry.

## The gap that is real

No verified prior work combines (a) legacy LV network reconstruction under incomplete observability with explicit data tiers, (b) engineering feasibility gating before cost comparison, (c) an incumbent-admissible optional estimand (VoF), and (d) urban spatial/morphological conditioning of that value. The honest increment is therefore *not* a theorem — it is a decision framework plus an empirical demonstration across three Japanese zones that the option value is bounded (<0.5% LCC) once feasibility and estimand are respected, and (new for CEUS) that this bound varies interpretably with measured urban spatial structure at feeder-cluster scale.

## Citation placement rules applied

- Introduction: morphology canon (Barthélemy, Cardillo, Louf, Boeing, Levinson) + renewal CBA (Larsen, Fenrick & Getachew) + undergrounding/resilience (Taheri) establish the policy and spatial setting.
- Methods: reconstruction precedents (Abhilash Bandam 2021; Zhang et al. 2025; Liu/TNO; Fu 2016 for spatial-network modelling) + planning methods (Samui, Kumar, Camargo, Tram & Wall, Baran & Wu) + LinDistFlow/Steiner foundations.
- Discussion: Abdel-Mottaleb & Zhang morphology-connectivity link + path-dependence DSS + bounded-result dialogue with Larsen/Fenrick.
- No CEUS papers cited merely to flatter; the two CAIE anchor works are cited because they define the reconstruction-neighbourhood the paper extends. CEUS-specific citations added only where they carry content (morphology metrics).
