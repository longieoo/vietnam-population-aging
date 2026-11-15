"""Negative checks for edited CSVs and corrupted cached source responses."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import acquire
import prepare
from analyze import demographic_insights
from config import ROOT


class MasterContractTests(unittest.TestCase):
    def frame(self):
        return prepare.add_features(pd.DataFrame({
            'iso3': ['VNM'], 'year': [2023], 'country': ['Vietnam'],
            'region': ['East Asia & Pacific'], 'income_group': ['Lower middle income'],
            'population': [1000.0], 'age_0_14': [20.0], 'age_15_64': [70.0],
            'age_65_plus': [10.0], 'fertility': [2.0], 'gdp_ppp': [5000.0],
            'lfpr': [75.0], 'employment': [70.0],
        }))

    def test_saved_snapshot_satisfies_contract(self):
        receipt = prepare.validate_master(pd.read_csv(ROOT / 'data/processed/master.csv'))
        self.assertEqual(receipt['derived_formulas_checked'], 4)
        self.assertEqual(receipt['source_indicators'], 8)

    def test_incomplete_vietnam_cannot_produce_published_findings(self):
        frame = pd.read_csv(ROOT / 'data/processed/master.csv')
        frame.loc[frame.iso3.eq('VNM') & frame.year.eq(2023), 'lfpr'] = np.nan
        with self.assertRaisesRegex(ValueError, 'missing required values'):
            demographic_insights(frame)

    def test_population_coverage_uses_complete_pair_not_single_indicator(self):
        frame = pd.read_csv(ROOT / 'data/processed/master.csv')
        selected = frame.iso3.eq('ABW') & frame.year.eq(2023)
        frame.loc[selected, ['age_65_plus', 'age_15_64']] = np.nan
        result = demographic_insights(frame)
        end = frame.loc[frame.year.eq(2023)]
        for columns, key in [(['gdp_ppp', 'age_65_plus'], 'gdp_sample_population_coverage_pct'),
                             (['employment', 'age_15_64'], 'labor_sample_population_coverage_pct')]:
            expected = end.dropna(subset=columns).population.sum() / end.population.sum() * 100
            self.assertAlmostEqual(result[key], expected)

    def test_missing_source_values_are_preserved(self):
        frame = self.frame()
        frame.loc[0, ['age_0_14', 'lfpr']] = np.nan
        frame = prepare.add_features(frame)
        prepare.validate_master(frame)
        self.assertTrue(pd.isna(frame.loc[0, 'total_dependency']))

    def test_invalid_grain_and_units_are_rejected(self):
        cases = {'iso3': None, 'year': 2023.5, 'country': '',
                 'population': np.inf, 'gdp_ppp': -1.0, 'employment': 101.0,
                 'age_0_14': 30.0, 'lfpr': 60.0}
        for column, value in cases.items():
            with self.subTest(column=column):
                frame = self.frame()
                if column == 'year':
                    frame['year'] = frame.year.astype(float)
                frame.loc[0, column] = value
                with self.assertRaises(ValueError):
                    prepare.validate_master(frame)

    def test_duplicate_keys_and_missing_columns_are_rejected(self):
        frame = self.frame()
        for invalid in [pd.concat([frame, frame]), frame.drop(columns='population')]:
            with self.assertRaises(ValueError):
                prepare.validate_master(invalid)

    def test_derived_value_and_missingness_corruption_are_rejected(self):
        for value in [999.0, np.nan]:
            frame = self.frame()
            frame.loc[0, 'old_dependency'] = value
            with self.assertRaisesRegex(ValueError, 'Derived formula'):
                prepare.validate_master(frame)
        frame = self.frame()
        frame.loc[0, 'age_65_plus'] = np.nan
        with self.assertRaisesRegex(ValueError, 'Derived formula'):
            prepare.validate_master(frame)


class CachedSourceTests(unittest.TestCase):
    def test_cache_is_bound_to_request_url(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'page.json'
            raw = b'[]'
            path.write_bytes(raw)
            path.with_suffix('.json.receipt.json').write_text(json.dumps({
                'url': 'https://example.org/original', 'bytes': len(raw),
                'sha256': hashlib.sha256(raw).hexdigest(),
            }), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'URL mismatch'):
                acquire.fetch('https://example.org/changed', path)

    def test_inconsistent_page_headers_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'data/raw').mkdir(parents=True)
            for number, total in [(1, 2), (2, 3)]:
                (root / f'data/raw/example_p{number}.json').write_text(json.dumps([
                    {'page': number, 'pages': 2, 'total': total}, [{'id': number}],
                ]), encoding='utf-8')
            with patch.object(prepare, 'ROOT', root):
                with self.assertRaisesRegex(ValueError, 'Inconsistent API page'):
                    prepare.read_pages('example')

    def test_manifest_path_cannot_escape_raw_directory(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'data/metadata').mkdir(parents=True)
            (root / 'data/metadata/source_manifest.json').write_text(json.dumps({
                'files': [{'path': '../outside', 'bytes': 0, 'sha256': ''}],
            }), encoding='utf-8')
            with patch.object(prepare, 'ROOT', root):
                with self.assertRaisesRegex(ValueError, 'outside data/raw'):
                    prepare.verify_snapshot()

    def test_atomic_cache_publication(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'nested/source.json'
            acquire.atomic_write(path, b'first')
            acquire.atomic_write(path, b'second')
            self.assertEqual(path.read_bytes(), b'second')
            self.assertEqual([item.name for item in path.parent.iterdir()], ['source.json'])


if __name__ == '__main__':
    unittest.main()
