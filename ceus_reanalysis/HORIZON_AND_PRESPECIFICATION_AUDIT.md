# Horizon & prespecification audit (Phase 3)
- primary_horizon_years = 40 (config/study.yaml), discount 0.03, load factor 0.35,
  electricity 25 JPY/kWh; 30/50 evaluated as horizon sensitivity.
- DEFECT FIXED: CAIE and CEUS manuscripts said "30-year discounted losses" in Methods.
  Corrected to "40-year discounted" in p13e/p17 builders; docx regenerated.
- "Prespecified" descriptor set: the Gate-3 morphology protocol
  (ceus_reassessment/CEUS_ADDITIONAL_ANALYSIS_PROTOCOL.md) was frozen before morphology
  results were generated, so "prespecified descriptor set" is accurate for the protocol.
  The v1 hull-density implementation defect means the density descriptor is superseded:
  v2 descriptors are reported as the protocol descriptor set plus a stable-support
  density added as a sensitivity descriptor, clearly labeled.
- No pre-registration claimed anywhere ("prespecified", not "pre-registered").
