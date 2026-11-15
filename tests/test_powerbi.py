"""Check that the retained Power BI delivery opens with its model and data intact."""
import hashlib
import json
from pathlib import Path
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]


class PowerBIDeliveryTests(unittest.TestCase):
    def test_pbip_resolves_report_and_model(self):
        project = ROOT / 'powerbi/PopulationAging.pbip'
        definition = json.loads(project.read_text('utf-8'))
        for artifact in definition['artifacts']:
            report = project.parent / artifact['report']['path']
            report_definition = json.loads((report / 'definition.pbir').read_text('utf-8'))
            model = report / report_definition['datasetReference']['byPath']['path']
            self.assertTrue((model / 'definition.pbism').is_file())
            pages = json.loads((report / 'definition/pages/pages.json').read_text('utf-8'))
            self.assertEqual(len(pages['pageOrder']), 6)
            self.assertIn(pages['activePageName'], pages['pageOrder'])
            visual_ids = set()
            for page in pages['pageOrder']:
                folder = report / 'definition/pages' / page
                self.assertTrue((folder / 'page.json').is_file(), page)
                for visual in folder.glob('visuals/*/visual.json'):
                    content = json.loads(visual.read_text('utf-8'))
                    identifier = (page, content['name'])
                    self.assertNotIn(identifier, visual_ids)
                    visual_ids.add(identifier)
            self.assertGreater(len(visual_ids), 0)

    def test_retained_pbix_is_intact_and_matches_its_receipt(self):
        receipt = json.loads((ROOT / 'powerbi/validation.json').read_text('utf-8'))
        pbix = ROOT / 'powerbi/PopulationAging.pbix'
        self.assertEqual(hashlib.sha256(pbix.read_bytes()).hexdigest(), receipt['pbix']['sha256'])
        self.assertEqual(hashlib.sha256((ROOT / 'data/processed/master.csv').read_bytes()).hexdigest(),
                         receipt['data']['master_sha256'], 'PBIX receipt has stale source data')
        with zipfile.ZipFile(pbix) as archive:
            self.assertIsNone(archive.testzip())
            self.assertIn('DataModel', archive.namelist())
            self.assertGreater(archive.getinfo('DataModel').file_size, 0)


if __name__ == '__main__':
    unittest.main()
