"""Material integrity checks, including source-to-slide chart numbers."""
import json
import re
import hashlib
import zipfile
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import nbformat
from config import ROOT, FOCAL, INDICATORS, YEARS
from prepare import verify_snapshot


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify_raw_values(master, root=None):
    """Independent reader: no preparation helpers or processed lookup tables."""
    root = ROOT if root is None else root
    def records(stem):
        files = sorted((root / 'data/raw').glob(stem + '_p*.json'))
        files = [p for p in files if re.fullmatch(re.escape(stem) + r'_p\d+\.json', p.name)]
        require(bool(files), 'Missing source pages: ' + stem)
        payloads = [json.loads(p.read_text('utf-8')) for p in files]
        expected = int(payloads[0][0]['pages'])
        require(sorted(int(p[0]['page']) for p in payloads) == list(range(1, expected+1)), 'Source page sequence: ' + stem)
        require(all(int(p[0]['pages']) == expected and int(p[0]['total']) == int(payloads[0][0]['total']) for p in payloads), 'Inconsistent page headers: ' + stem)
        result = [r for p in payloads for r in (p[1] or [])]
        require(len(result) == int(payloads[0][0]['total']), 'Source row count: ' + stem)
        return result
    eligible = {r['id'] for r in records('countries') if r['region']['id'] != 'NA' and r['region']['value'] != 'Aggregates'}
    data = {}
    for variable, code in INDICATORS.items():
        for r in records(variable):
            require(r['indicator']['id'] == code, 'Unexpected indicator in ' + variable)
            key = (r['countryiso3code'], int(r['date']))
            if key[0] not in eligible or key[1] not in YEARS:
                continue
            require(variable not in data.setdefault(key, {}), 'Duplicate source key: ' + str(key))
            data[key][variable] = r['value']
    data = {k:v for k,v in data.items() if any(x is not None for x in v.values())}
    expected = pd.DataFrame([dict(iso3=k[0],year=k[1],**v) for k,v in data.items()]).set_index(['iso3','year']).sort_index()
    actual = master.set_index(['iso3','year']).sort_index()
    require(actual.index.is_unique and actual.index.equals(expected.index), 'Raw/master key mismatch')
    for variable in INDICATORS:
        require(np.allclose(actual[variable], expected[variable], rtol=1e-10, atol=1e-10, equal_nan=True), 'Raw/master values differ: ' + variable)
    formulas = {
        'population_65_plus': expected.population * expected.age_65_plus / 100,
        'child_dependency': 100 * expected.age_0_14 / expected.age_15_64.where(expected.age_15_64 > 0),
        'old_dependency': 100 * expected.age_65_plus / expected.age_15_64.where(expected.age_15_64 > 0),
        'total_dependency': 100 * (expected.age_0_14 + expected.age_65_plus) / expected.age_15_64.where(expected.age_15_64 > 0),
    }
    for variable, values in formulas.items():
        require(np.allclose(actual[variable], values, rtol=1e-10, atol=1e-9, equal_nan=True), 'Derived formula differs: ' + variable)
    return len(expected) * len(INDICATORS)


def verify_notebook_provenance(notebook, master_path, snapshot):
    provenance = notebook.metadata.get('aging_provenance', {})
    digest = hashlib.sha256(master_path.read_bytes()).hexdigest()
    require(provenance.get('master_sha256') == digest, 'Notebook is stale: rebuild with --notebook (master SHA mismatch)')
    require(provenance.get('source_snapshot') == snapshot, 'Notebook source snapshot mismatch')
    return digest


def verify_new_insights(master, summary):
    insight = summary.get('demographic_insights')
    if insight is None:
        return 0
    vn = master.loc[master.iso3.eq('VNM')].set_index('year')
    a,b = vn.loc[1991],vn.loc[2023]
    component_p = (b.population-a.population)*(b.age_65_plus+a.age_65_plus)/200
    component_s = (b.age_65_plus-a.age_65_plus)*(b.population+a.population)/200
    expected = {'population_component':component_p, 'age_structure_component':component_s,
        'older_population_increase':component_p+component_s,
        'recent_aging_change_pp':b.age_65_plus-vn.loc[2010,'age_65_plus'],
        'recent_fraction_of_full_change_pct':100*(b.age_65_plus-vn.loc[2010,'age_65_plus'])/(b.age_65_plus-a.age_65_plus)}
    low=vn.loc[vn.total_dependency.idxmin()]
    expected.update(dependency_increase_since_min=b.total_dependency-low.total_dependency,
        old_dependency_increase_since_peak=b.old_dependency-low.old_dependency,
        old_dependency_fraction_of_rebound_pct=100*(b.old_dependency-low.old_dependency)/(b.total_dependency-low.total_dependency),
        lfpr_change_2019_2023_pp=b.lfpr-vn.loc[2019,'lfpr'],
        employment_change_2019_2023_pp=b.employment-vn.loc[2019,'employment'])
    for key, value in expected.items():
        require(np.isclose(insight[key],value,rtol=1e-9), 'Demographic insight mismatch: '+key)
    return len(expected)


def verify_native_slides(master, path):
    """Check editable PPTX chart caches when a native deck is supplied."""
    with zipfile.ZipFile(path) as z:
        ns = {'c': 'http://schemas.openxmlformats.org/drawingml/2006/chart'}
        charts = sorted([n for n in z.namelist() if re.search('/charts/chart\\d+\\.xml$', n)], key=lambda n: int(re.search('chart(\\d+)\\.xml', n).group(1)))
        if not len(charts) == 11:
            raise ValueError('Delivery validation failed: len(charts) == 11')
        values = []
        for chart in charts:
            tree = ET.fromstring(z.read(chart))
            arr = []
            for series in tree.findall('.//c:ser', ns):
                v = series.find('c:yVal', ns)
                if v is None:
                    v = series.find('c:val', ns)
                arr.append([float(e.text) for e in v.findall('.//c:pt/c:v', ns)])
            values.append(arr)
        vn = master[master.iso3.eq('VNM')].sort_values('year')
        expected = []
        expected.append([vn[c].tolist() for c in ['age_0_14', 'age_15_64', 'age_65_plus']])
        expected.append([(vn.population_65_plus / 1000000.0).tolist()])
        expected.append([vn[c].tolist() for c in ['child_dependency', 'old_dependency', 'total_dependency']])
        expected.append([[master[(master.iso3 == c) & (master.year == y)].age_65_plus.iloc[0] for c in FOCAL] for y in [1991, 2023]])
        expected.append([master[master.iso3.eq(c)].sort_values('year').fertility.tolist() for c in FOCAL])
        cross = pd.read_csv(ROOT / 'outputs/tables/gdp_aging_2023.csv')
        expected.append([cross[~cross.iso3.isin(FOCAL)].age_65_plus.tolist()] + [[cross[cross.iso3.eq(c)].age_65_plus.iloc[0]] for c in FOCAL])
        bench = pd.read_csv(ROOT / 'outputs/tables/threshold_crossings.csv')
        funnel_path = ROOT / 'outputs/tables/threshold_sample_funnel.csv'
        if funnel_path.exists():
            wanted_funnel = bench.assign(gdp_available=bench.gdp_ppp.notna()).groupby(['threshold','status','gdp_available']).size().rename('economies').reset_index()
            actual_funnel = pd.read_csv(funnel_path)
            require(actual_funnel.equals(wanted_funnel), 'Threshold sample funnel mismatch')
        expected.append([[bench[(bench.iso3 == c) & (bench.threshold == 10)].gdp_ppp.iloc[0] for c in ['THA', 'KOR']]])
        expected.extend([[vn[c].tolist()] for c in ['age_15_64', 'lfpr', 'employment']])
        expected.append([pd.read_csv(ROOT / 'outputs/tables/labor_2023.csv').employment.tolist()])
        for ci, (actual, wanted) in enumerate(zip(values, expected)):
            if not len(actual) == len(wanted):
                raise ValueError('Delivery validation failed: ci')
            for aa, ww in zip(actual, wanted):
                if not np.allclose(aa, ww, rtol=0, atol=5.1e-07):
                    raise ValueError('Delivery validation failed: (ci, aa[:2], ww[:2])')
        for index in [1, 2, 4, 7, 8, 9]:
            tree = ET.fromstring(z.read(charts[index]))
            for series in tree.findall('.//c:ser', ns):
                xx = [float(e.text) for e in series.findall('./c:xVal//c:pt/c:v', ns)]
                if not xx == list(range(1991, 2024)):
                    raise ValueError('Delivery validation failed: index')
        tree = ET.fromstring(z.read(charts[5]))
        xs = []
        for ser in tree.findall('.//c:ser', ns):
            xs.append([float(e.text) for e in ser.findall('./c:xVal//c:pt/c:v', ns)])
        wanted = [np.log10(cross[~cross.iso3.isin(FOCAL)].gdp_ppp).tolist()] + [[np.log10(cross[cross.iso3.eq(c)].gdp_ppp.iloc[0])] for c in FOCAL]
        for aa, ww in zip(xs, wanted):
            if not np.allclose(aa, ww, rtol=0, atol=5.1e-07):
                raise ValueError('Delivery validation failed: np.allclose(aa, ww, rtol=0, atol=5.1e-07)')
        if not len([n for n in z.namelist() if n.startswith('ppt/embeddings/') and n.endswith('.xlsx')]) == 11:
            raise ValueError("Delivery validation failed: len([n for n in z.namelist() if n.startswith('ppt/embeddings/') and n.endswith('.xlsx')]) == 11")
    with zipfile.ZipFile(path) as z:
        tree = ET.fromstring(z.read(charts[10]))
        labor_x = [float(e.text) for e in tree.findall('.//c:ser/c:xVal//c:pt/c:v', ns)]
        labor = pd.read_csv(ROOT / 'outputs/tables/labor_2023.csv')
        require(len(labor_x) == len(labor) and np.allclose(labor_x, labor.age_15_64, rtol=0, atol=.00000051), 'Labor slide x coordinates differ')
    return {'status': 'passed', 'native_charts_checked_against_tables': 11, 'embedded_workbooks': 11}


def main():
    manifest = verify_snapshot()
    master = pd.read_csv(ROOT / 'data/processed/master.csv')
    raw_cells = verify_raw_values(master)
    s = json.loads((ROOT / 'outputs/tables/analysis_summary.json').read_text())
    q = json.loads((ROOT / 'outputs/tables/quality_summary.json').read_text())
    if not (len(master) == q['meaningful_rows'] and master.iso3.nunique() == q['economies']):
        raise ValueError("Delivery validation failed: len(master) == q['meaningful_rows'] and master.iso3.nunique() == q['economies']")
    if not not master.duplicated(['iso3', 'year']).any():
        raise ValueError("Delivery validation failed: not master.duplicated(['iso3', 'year']).any()")
    checks = pd.read_csv(ROOT / 'outputs/tables/vietnam_source_checks.csv')
    if not (checks.matches.all() and len(checks) == 16):
        raise ValueError('Delivery validation failed: checks.matches.all() and len(checks) == 16')
    notebook = nbformat.read(ROOT / 'notebooks/analysis.ipynb', as_version=4)
    nbformat.validate(notebook)
    master_sha = verify_notebook_provenance(notebook, ROOT / 'data/processed/master.csv', manifest['snapshot_id'])
    insight_checks = verify_new_insights(master, s)
    for filename, columns in [('gdp_aging_2023', ['gdp_ppp','age_65_plus']), ('labor_2023', ['age_15_64','employment'])]:
        actual_sample = pd.read_csv(ROOT / f'outputs/tables/{filename}.csv').set_index('iso3').sort_index()
        expected_sample = master.loc[master.year.eq(2023)].dropna(subset=columns).set_index('iso3').sort_index()
        require(actual_sample.index.equals(expected_sample.index), 'Sample keys differ: '+filename)
        for column in columns:
            require(np.allclose(actual_sample[column], expected_sample[column], rtol=1e-10, atol=1e-10), 'Sample values differ: '+filename+'/'+column)

    funnel_path = ROOT / 'outputs/tables/threshold_sample_funnel.csv'
    if funnel_path.exists():
        bench = pd.read_csv(ROOT / 'outputs/tables/threshold_crossings.csv')
        wanted = bench.assign(gdp_available=bench.gdp_ppp.notna()).groupby(['threshold', 'status', 'gdp_available']).size().rename('economies').reset_index()
        require(pd.read_csv(funnel_path).equals(wanted), 'Threshold sample funnel mismatch')

    cells = [c for c in notebook.cells if c.cell_type == 'code']
    if not all((c.execution_count is not None for c in cells)):
        raise ValueError('Delivery validation failed: all((c.execution_count is not None for c in cells))')
    if not not any((o.output_type == 'error' for c in cells for o in c.outputs)):
        raise ValueError("Delivery validation failed: not any((o.output_type == 'error' for c in cells for o in c.outputs))")
    slide_path = ROOT / 'slides/presentation.pptx'
    slides = verify_native_slides(master, slide_path) if slide_path.is_file() else {
        'status': 'not_applicable', 'reason': 'Presentation is maintained on Canva; remote slide content is not validated locally.',
        'native_charts_checked_against_tables': 0, 'embedded_workbooks': 0}
    from config import format_number as f
    text = (ROOT / 'reports/report_submission.md').read_text('utf-8')
    headlines = [s['vietnam_1991']['age_65_plus'], s['vietnam_2023']['age_65_plus'], s['vietnam_old_share_change_pp'], s['vietnam_gdp_multiplier'], s['robustness'][0]['pearson'], s['robustness'][3]['pearson']]
    if not all((f(v) in text for v in headlines)):
        raise ValueError('Delivery validation failed: all((f(v) in text for v in headlines))')
    if not len(list((ROOT / 'outputs/figures').glob('*.png'))) == 12:
        raise ValueError("Delivery validation failed: len(list((ROOT / 'outputs/figures').glob('*.png'))) == 12")
    if not len(list((ROOT / 'outputs/figures').glob('*.svg'))) == 12:
        raise ValueError("Delivery validation failed: len(list((ROOT / 'outputs/figures').glob('*.svg'))) == 12")
    evidence = pd.read_csv(ROOT / 'outputs/tables/evidence_table.csv')
    if not len(evidence) == 7:
        raise ValueError('Delivery validation failed: len(evidence) == 7')
    result = {'snapshot_id': manifest['snapshot_id'], 'source_files_verified': len(manifest['files']), 'unique_rows': len(master), 'vietnam_source_values_matched': len(checks), 'executed_code_cells': len(cells), 'principal_png_figures': 12, 'principal_svg_figures': 12, 'presentation': slides, 'native_charts_checked_against_tables': slides['native_charts_checked_against_tables'], 'embedded_workbooks': slides['embedded_workbooks'], 'headline_values_traced': len(headlines), 'raw_indicator_cells_checked': raw_cells, 'derived_formulas_checked': 4, 'notebook_master_sha256': master_sha, 'demographic_insights_checked': insight_checks, 'status': 'passed'}
    (ROOT / 'outputs/tables/delivery_validation.json').write_text(json.dumps(result, indent=2), 'utf-8')
    print(json.dumps(result, indent=2))
if __name__ == '__main__':
    main()
