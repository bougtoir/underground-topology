# Numerical tolerance spec (Gate 1B)
VoF = max(0, NPC_S1 - NPC_S2) per replicate mean; reported as % of S1 NPC.
Two clusters carry vof_pct ~1e-15% (kudamatsu c13: 4.97e-9 JPY, yasu c105:
6.2e-10 JPY) — orders below the reporting precision (0.001%) and below any
economic resolution (~1 JPY on ~bn-JPY NPCs). Classification rule (NOT
prespecified; declared as computational rule): vof_pct > 1e-4 counts as
positive. Robustness: thresholds 1e-6/1e-4/1e-3 all give 24 positives
(3 sano, 13 kudamatsu, 8 yasu); inference unaffected. Tolerance is relative
(to NPC share), appropriate since s1_npc varies across clusters.
