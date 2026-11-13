import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import unittest
import numpy as np
import pandas as pd
from prepare import add_features, first_crossing, verify_snapshot
from config import ROOT

class CalculationTests(unittest.TestCase):
    def test_dependencies_and_population(self):
        x = add_features(pd.DataFrame({'population':[1000], 'age_0_14':[20], 'age_15_64':[70], 'age_65_plus':[10]})).iloc[0]
        self.assertAlmostEqual(x.population_65_plus,100)
        self.assertAlmostEqual(x.total_dependency,300/7)
        self.assertAlmostEqual(x.old_dependency,100/7)
    def frame(self,years,shares,gdp=None):
        return pd.DataFrame({'year':years,'age_65_plus':shares,'gdp_ppp':gdp or [5000]*len(years)})
    def test_observed_crossing(self):
        self.assertEqual(first_crossing(self.frame([1991,1992,1993],[9,10,11]))['year'],1992)
    def test_left_censoring(self):
        self.assertEqual(first_crossing(self.frame([1991,1992],[11,12]))['status'],'already_above')
    def test_not_reached(self):
        self.assertEqual(first_crossing(self.frame([1991,1992],[8,9]))['status'],'not_reached')
    def test_gap_and_missing_gdp(self):
        r=first_crossing(self.frame([1991,1993],[9,11],[5000,np.nan]))
        self.assertEqual(r['status'],'gap_uncertain')
        self.assertIsNone(r['gdp_ppp'])
    def test_prior_gap_can_hide_crossing(self):
        self.assertEqual(first_crossing(self.frame([1991,1993,1994],[8,9,11]))['status'],'gap_uncertain')
    def test_snapshot_and_master(self):
        verify_snapshot()
        d=pd.read_csv(ROOT/'data/processed/master.csv')
        self.assertFalse(d.duplicated(['iso3','year']).any())
        self.assertGreaterEqual(len(d),5000)
        self.assertTrue(np.allclose(d.total_dependency,(d.age_0_14+d.age_65_plus)/d.age_15_64*100,equal_nan=True))

if __name__ == '__main__': unittest.main()
