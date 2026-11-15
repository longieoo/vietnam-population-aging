"""Source-bound offline dashboard verification; no browser/runtime dependency."""
import hashlib
import json
import unittest
from pathlib import Path
from html.parser import HTMLParser
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]

class PayloadParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.inside = False
        self.parts = []
        self.external_scripts = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'script':
            self.inside = attrs.get('id') == 'data'
            if 'src' in attrs:
                self.external_scripts.append(attrs['src'])
    def handle_endtag(self, tag):
        if tag == 'script':
            self.inside = False
    def handle_data(self, data):
        if self.inside:
            self.parts.append(data)

class DashboardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT/'outputs/interactive/explorer.html').read_text('utf-8')
        cls.parser = PayloadParser()
        cls.parser.feed(cls.html)
        cls.payload = json.loads(''.join(cls.parser.parts))
        cls.master = pd.read_csv(ROOT/'data/processed/master.csv')

    def test_dashboard_snapshot_and_all_source_columns(self):
        payload = self.payload
        self.assertEqual(payload['master_sha256'], hashlib.sha256((ROOT/'data/processed/master.csv').read_bytes()).hexdigest())
        actual = pd.DataFrame(payload['rows'])
        self.assertEqual(len(actual), len(self.master))
        self.assertEqual(actual[['iso3','year']].to_dict('records'), self.master[['iso3','year']].to_dict('records'))
        for col in self.master.select_dtypes(include='number').columns:
            np.testing.assert_allclose(actual[col], self.master[col], rtol=1e-13, atol=1e-12, equal_nan=True)

    def test_derived_metrics_preserve_missing_and_denominators(self):
        actual = pd.DataFrame(self.payload['rows'])
        np.testing.assert_allclose(actual.aging_index, self.master.age_65_plus/self.master.age_0_14*100, equal_nan=True)
        np.testing.assert_allclose(actual.potential_support_ratio, self.master.age_15_64/self.master.age_65_plus, equal_nan=True)
        self.assertEqual(actual.employment.isna().sum(), self.master.employment.isna().sum())
        self.assertEqual(actual.gdp_ppp.isna().sum(), self.master.gdp_ppp.isna().sum())

    def test_embedded_logic_current_and_runtime_offline(self):
        self.assertEqual(self.parser.external_scripts, [])
        for name in ['dashboard_model.js','dashboard_app.js']:
            self.assertIn((ROOT/'src'/name).read_text('utf-8'), self.html)
        for view in ['overview','aging','economy','labor']:
            self.assertIn('id="tab-'+view+'"', self.html)
        self.assertEqual(self.payload['crossings'], json.loads(pd.read_csv(ROOT/'outputs/tables/threshold_crossings.csv').to_json(orient='records',force_ascii=False,double_precision=15)))

    def test_keyboard_tabs_and_source_pagination_available(self):
        for token in ['id="source-prev"', 'id="source-next"', 'id="source-page"', 'class="skip-link"', 'prefers-reduced-motion']:
            self.assertIn(token, self.html)
        self.assertEqual(self.html.count('tabindex="-1" aria-controls="dashboard"'), 3)

    def test_csv_fallbacks_match_the_named_fixed_samples(self):
        for name, fields in [('gdp',['gdp_ppp','age_65_plus']),('labor',['age_15_64','employment'])]:
            expected = self.master.loc[self.master.year.eq(2023)].dropna(subset=fields)
            actual = pd.read_csv(ROOT/f'outputs/tables/dashboard_{name}_2023.csv')
            self.assertEqual(actual.iso3.tolist(), expected.iso3.tolist())
            for field in fields:
                np.testing.assert_allclose(actual[field], expected[field])

if __name__ == '__main__':
    unittest.main()
