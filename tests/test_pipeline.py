"""Exercise actual subprocess failures and ZIP integrity with isolated files."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from pipeline import Runner
from package_delivery import package, verify_archive

class PipelineTests(unittest.TestCase):
    def test_failure_records_nonzero_exit_and_stops(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            runner = Runner(root, env={})
            with self.assertRaises(subprocess.CalledProcessError):
                runner.run('failure', [sys.executable, '-c', 'raise SystemExit(7)'])
                runner.run('must_not_run', [sys.executable, '-c', 'pass'])
            receipt = json.loads((root / 'work/logs/build-receipt.json').read_text())
            self.assertEqual(receipt['status'], 'failed')
            self.assertEqual(len(receipt['steps']), 1)
            self.assertEqual(receipt['steps'][0]['status'], 'failed')

    def test_portable_package_excludes_runtime_and_detects_tampering(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / 'project'
            (root / 'work').mkdir(parents=True)
            (root / 'work/private-cache.txt').write_text('exclude')
            (root / 'README.md').write_text('portable project')
            result = package(root)
            archive = Path(result['archive'])
            self.assertEqual(verify_archive(archive), 1)
            with zipfile.ZipFile(archive) as z:
                entries = {name: z.read(name) for name in z.namelist()}
            entries['project/README.md'] = b'tampered'
            with zipfile.ZipFile(archive, 'w') as z:
                for name, content in entries.items():
                    z.writestr(name, content)
            with self.assertRaisesRegex(ValueError, 'Checksum mismatch'):
                verify_archive(archive)

    def test_output_inside_project_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with self.assertRaisesRegex(ValueError, 'outside'):
                package(root, root / 'recursive.zip')

if __name__ == '__main__':
    unittest.main()
