# 130-kVA variant root cause (Gate 3)
Trace: t130 sensitivity run predates the VoF estimand —
cluster_results_t130.csv has NO vof_mean column at all, and EVERY qualifying
cluster is single-terminal (sano 78, kudamatsu 2, yasu 10 rows; terminals=1
throughout). With one demand terminal there is no topology choice: S1==S2
trivially (s2_npc == s1_npc_mean for all rows, s2_length 0... wait s2_length
equals s1 in all rows). Hence vof_pct is legitimately undefined (NaN), and
ltp_pct=0.0 is trivially zero — NOT a bug and NOT a robustness result.
Action: Table 4 keeps the rows but renders "n/a" for VoF with footnote
explaining the boundary case; no zeros interpolated, no re-run (nothing to fix).
