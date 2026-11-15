"""Negative tests isolate corruption in temporary directories, never the snapshot."""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import nbformat
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import prepare
from verify_delivery import require, verify_notebook_provenance, verify_raw_values


class IntegrityTests(unittest.TestCase):
    def test_corrupt_snapshot_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'data/metadata').mkdir(parents=True)
            (root / 'data/raw').mkdir(parents=True)
            source = root / 'data/raw/source.json'
            source.write_bytes(b'original')
            manifest = {'files': [{'path': 'data/raw/source.json', 'bytes': len(b'original'), 'sha256': hashlib.sha256(b'original').hexdigest()}]}
            (root / 'data/metadata/source_manifest.json').write_text(json.dumps(manifest))
            source.write_bytes(b'corrupt!')
            with patch.object(prepare, 'ROOT', root), self.assertRaisesRegex(ValueError, 'checksum mismatch'):
                prepare.verify_snapshot()

    def test_missing_page_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'data/raw').mkdir(parents=True)
            (root / 'data/raw/example_p1.json').write_text(json.dumps([{'pages': 2, 'page': 1, 'total': 2}, [{'x': 1}]]))
            with patch.object(prepare, 'ROOT', root), self.assertRaisesRegex(ValueError, 'Incomplete pages'):
                prepare.read_pages('example')

    def test_duplicate_threshold_year_is_rejected(self):
        frame = pd.DataFrame({'year': [1991, 1991], 'age_65_plus': [9, 11], 'gdp_ppp': [100, 200]})
        with self.assertRaisesRegex(ValueError, 'Duplicate years'):
            prepare.first_crossing(frame)

    def test_missing_beginning_is_uncertain(self):
        frame = pd.DataFrame({'year': [1991, 1992, 1993], 'age_65_plus': [None, 9, 11], 'gdp_ppp': [100, 200, 300]})
        self.assertEqual(prepare.first_crossing(frame)['status'], 'gap_uncertain')

    def test_stale_notebook_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'master.csv'
            source.write_bytes(b'current data')
            notebook = nbformat.v4.new_notebook(metadata={'aging_provenance': {'master_sha256': 'outdated', 'source_snapshot': 'snapshot'}})
            with self.assertRaisesRegex(ValueError, 'Notebook is stale'):
                verify_notebook_provenance(notebook, source, 'snapshot')

    def test_validation_remains_active_under_optimization(self):
        src = str(Path(__file__).resolve().parents[1] / 'src')
        code = f"import sys;sys.path.insert(0,{src!r});from verify_delivery import require;require(False,'intentional integrity failure')"
        result = subprocess.run([sys.executable, '-O', '-c', code], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('intentional integrity failure', result.stderr)

    def test_all_raw_values_match(self):
        root = Path(__file__).resolve().parents[1]
        frame = pd.read_csv(root / 'data/processed/master.csv')
        self.assertEqual(verify_raw_values(frame, root), len(frame) * 8)
        damaged = frame.copy()
        damaged.loc[0, 'population'] += 1000
        with self.assertRaisesRegex(ValueError, 'Raw/master values differ'):
            verify_raw_values(damaged, root)


if __name__ == '__main__':
    unittest.main()
