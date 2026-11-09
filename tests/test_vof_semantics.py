"""Independent checks of the VoF estimand (JIS semantic audit).

1. Synthetic: VoF = max(0, NPC(S1) - min NPC(S2)) is >= 0 and equals the
   naive contrast only when redesign is cheaper.
2. Canonical: zone-level VoF%, denominators and zero-mass counts in
   analysis/*.csv are re-derived from cluster-level results.
"""
import os
import unittest

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZONES = ["sano", "kudamatsu", "yasu"]
POS_TOL = 1e-6  # VoF % below this is floating-point zero


def vof(s1_npcs, s2_best):
    return sum(max(0.0, s - s2_best) for s in s1_npcs) / len(s1_npcs)


class SyntheticVoF(unittest.TestCase):
    def test_redesign_cheaper(self):
        self.assertAlmostEqual(vof([100.0, 110.0], 90.0), 15.0)

    def test_redesign_dearer_is_zero_not_negative(self):
        self.assertEqual(vof([100.0], 130.0), 0.0)
        self.assertLess(100.0 - 130.0, 0.0)  # naive contrast would be negative

    def test_mixed_replicates(self):
        self.assertAlmostEqual(vof([100.0, 80.0], 90.0), 5.0)


class CanonicalVoF(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sr = pd.read_csv(f"{ROOT}/analysis/scenario_results_v2.csv").set_index("city")
        cls.zm = pd.read_csv(f"{ROOT}/analysis/CEUS_ZERO_MASS_SUMMARY.csv").set_index("city")
        cls.rc = {z: pd.read_csv(f"{ROOT}/data/processed/{z}/cluster_results_v2.csv") for z in ZONES}

    def feas(self, z):
        rc = self.rc[z]
        return rc[rc.s2_feasible & (rc.n_s1_feas > 0)]

    def test_counts_and_vof_pct(self):
        tot, tot_f, tot_nt, pos = 0, 0, 0, 0
        for z in ZONES:
            f = self.feas(z)
            tot += len(self.rc[z]); tot_f += len(f); tot_nt += int((f.terminals > 1).sum())
            self.assertEqual(len(f), self.sr.loc[z, "clusters_feasible"])
            v = 100 * f.vof_mean.sum() / f.s1_npc_feas_mean.sum()
            self.assertAlmostEqual(v, self.sr.loc[z, "vof_pct"], places=9)
            self.assertGreaterEqual(f.vof_mean.min(), 0.0)
            p = int(((100 * f.vof_mean / f.s1_npc_feas_mean) > POS_TOL).sum())
            self.assertEqual(p, self.zm.loc[z, "positive_vof"]); pos += p
        self.assertEqual((tot, tot_f, tot_nt, pos), (589, 554, 336, 24))

    def test_feasible_incumbents_respect_gates(self):
        for z in ZONES:
            f = self.feas(z)
            self.assertLessEqual(f.s1_vdrop_max.max(), 6.0)
            self.assertLessEqual(f.s2_vdrop.max(), 6.0)

    def test_demand_denominators(self):
        all_mw = sum(self.rc[z].raw_kw.sum() for z in ZONES) / 1e3
        feas_mw = sum(self.feas(z).raw_kw.sum() for z in ZONES) / 1e3
        self.assertAlmostEqual(all_mw, 58.635, places=2)
        self.assertAlmostEqual(feas_mw, 49.56, places=1)


if __name__ == "__main__":
    unittest.main()
